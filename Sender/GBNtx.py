import socket
from Packet import Packet
from Constants import *

import sched
import threading
import time

class GBNtx:

    def __init__(self,filenm,N,MSS,server_hostname,server_port=7735):
        self.server_addr=(server_hostname,server_port)
        self.N = N
        self.MSS = MSS

        self.reader = open(filenm,'r')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 7000))

        self.window = []
        self.Sb = 0
        self.Sm = N -1

        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.timer_ev = None

        self.eof = False


    def __del__(self):
        self.reader.close()
        self.sock.close()


    #Send all the packets in the window
    def send_window(self,start=0):
        for p in self.window[start:]:
            self.sock.sendto(p.generate_udp_payload(), self.server_addr)
            print "Sending PKT %d" % (p.seq_num)



    #Update window by removing n packets from front and adding at the end
    def update_window(self,n_pkts):
        new_pkts = []
        for i in range(n_pkts):
            p = self.get_packet()
            if p:
                new_pkts.append(p)
                #Send data
                self.sock.sendto(p.generate_udp_payload(), self.server_addr)
                print "Sending PKT %d"%(p.seq_num)

        #Delete elments at the beginning
        del self.window[:n_pkts]

        #append the new list to the window
        self.window = self.window + new_pkts

        #update alarm
        if self.timer_ev:
            self.scheduler.cancel(self.timer_ev)
        self.timer_ev = self.scheduler.enter(TIME_OUT,1,self.send_window,())

        return len(new_pkts)









    def start(self):
        #TODO:if the file size is less than N packets, need to be handled
        # add the first N packets
        for i in range(self.N):
            p = self.get_packet()
            self.window.append(p)

        #Send the packets in the window
        self.send_window()

        while len(self.window)>0:
            # receive data from client
            data, addr = self.sock.recvfrom(4096)

            #create ACK packet from the received data
            p = Packet.build_packet(data,is_ack=True)

            if(p.seq_num > self.Sb):
                print "Rcvd ACK %d. Moving forward"%(p.seq_num)
                new_pkts = self.update_window(p.seq_num-self.Sb)
                self.Sm = self.Sm + new_pkts
                self.Sb = p.seq_num
            else:
                print "Wrong ACK %d rcvd"%(p.seq_num)



    def get_packet(self):
        if self.eof:
            return None

        data = ''
        #Read till MSS is reached or EOF is reached
        while(len(data)<=self.MSS-8 and not self.eof):
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


g = GBNtx("../UT/RFC 882.txt", 10, 512,'127.0.0.1')

g.start()
