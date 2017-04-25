import os
import sys
sys.path.append(os.path.abspath('../'))

import socket
from Packet import Packet
from Constants import *

import sched
import threading
import time
import thread
from Utils import *
import logging

class GBNtx:

    def __init__(self,filenm,N,MSS,server_hostname,server_port=7735):
        self.server_addr=(server_hostname,server_port)
        self.N = N
        self.MSS = MSS

        self.reader = open(filenm,'r')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.my_ip = get_my_ip()
        # print "My IP = %s"%self.my_ip
        self.sock.bind((self.my_ip, 7000))
        # self.sock.bind(('127.0.0.1', 7000))
        self.window = []
        self.win_head = 0
        self.win_tail = -1#N -1

        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.timer_ev = None

        self.eof = False

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Sender")
        self.logger.disabled = True


    def __del__(self):
        self.reader.close()
        self.sock.close()


    #Send all the packets in the window
    def send_window(self,start=0):
        # print "Time Out. Sending packets"
        for p in self.window[start:]:
            self.sock.sendto(p.generate_udp_payload(), self.server_addr)
            print "Timeout, sequence number = %d" % (p.seq_num)



    #Update window by removing n packets from front and adding at the end
    def update_window(self,n_pkts):
        if(n_pkts == 0):
            return n_pkts

            self.logger.info( "Update window : %d"%(n_pkts))

        new_pkts = []
        for i in range(n_pkts):
            p = self.get_packet()
            if p:
                new_pkts.append(p)
                #Send data
                self.sock.sendto(p.generate_udp_payload(), self.server_addr)
                self.logger.info("Sending PKT %d"%(p.seq_num))

        #Delete elments at the beginning
        if len(self.window)>0:
            del self.window[:n_pkts]

        #append the new list to the window
        self.window = self.window + new_pkts

        #update alarm
        if not self.scheduler.empty():
            self.scheduler.cancel(self.timer_ev)
            self.timer_ev = self.scheduler.enter(TIME_OUT,1,self.send_window,())
            self.scheduler.run()

        return len(new_pkts)









    def start(self):
        #TODO:if the file size is less than N packets, need to be handled
        # add the first N packets
        for i in range(self.N):
            p = self.get_packet()
            self.window.append(p)
            self.win_tail = self.win_tail + 1
            if self.eof:
                break


        #Send the packets in the window
        self.send_window()
        thread.start_new_thread(self.alram_trigerrer,())

        while len(self.window)>0:
            # receive data from client
            data, addr = self.sock.recvfrom(4096)

            #create ACK packet from the received data
            p = Packet.build_packet(data,is_ack=True)

            if(p.seq_num > self.win_head):
                new_pkts = self.update_window(p.seq_num - self.win_head)
                self.win_tail = self.win_tail + new_pkts
                self.win_head = p.seq_num
                self.logger.info( "Rcvd ACK %d. Moving forward to %d" % (p.seq_num,self.win_tail))

            else:
                self.logger.info( "Wrong ACK %d rcvd"%(p.seq_num))
                pass


    def get_packet(self):
        if self.eof:
            return None

        data = ''
        #Read till MSS is reached or EOF is reached
        while(len(data)<=self.MSS and not self.eof):
            c = self.rdt_send()
            if c == '':
                self.reader.close()
                c = TERMINATOR
                self.eof = True
            data = data + c

        p = Packet(data)
        return p



    def rdt_send(self):
        s = self.reader.read(1)
        return s

    def alram_trigerrer(self):
        while len(self.window)>0:
            if self.scheduler.empty():
                self.timer_ev = self.scheduler.enter(TIME_OUT, 1, self.send_window, ())
                #Bug fix
                if not self.scheduler.empty():
                    self.scheduler.run()
            time.sleep(TIME_OUT/2)


if __name__ == "__main__":
    if len(sys.argv)<6:
        print "Usage:"
        print "%s <server-hostname> <server-port> <file> <N> <MSS>"%(sys.argv[0])
        exit(-1)

    s_ip = sys.argv[1]
    s_port = int(sys.argv[2])
    filenm = sys.argv[3]
    N = int(sys.argv[4])
    MSS = int(sys.argv[5])

    g = GBNtx(filenm, N, MSS,s_ip,s_port)

    start_time = time.time()
    g.start()
    end_time = time.time()
    del g

    print "Transfer completed in %f seconds"%(end_time-start_time)
