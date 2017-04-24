import os
import sys
sys.path.append(os.path.abspath('../'))

from Packet import Packet
import socket
from Constants import *
import array
import random
from Utils import *

class GBNrx:
    def __init__(self, filnm, err_prob, port=7735):
        self.Rn = 0 # expected Request number
        self.port = port
        self.writer = open(filnm,'w+')
        self.err_prob = err_prob

        self.my_ip = get_my_ip()
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1',port))

        self.eof = False


    def start(self):
        while not self.eof:
            #receive data from server
            data, addr = self.sock.recvfrom(4096)

            # print "Data: %s"%data

            #create a packet from the data
            p = Packet.build_packet(data)
            # print p

            if self.discard_pkt():
                print "Packet loss, sequence number = %d"%p.seq_num
                continue

            self.process_pkt(p,addr)

        self.writer.close()
        self.sock.close()



    # Checks if the given packet was in the expected order
    def process_pkt(self,pkt,addr):
        if pkt.seq_num == self.Rn and pkt.valid_checksum() :
            #Increment value of Rn
            self.Rn = self.Rn +1
            print "PKT %d successfully received"%(pkt.seq_num)

            #ensure that the last packet is received in order
            if pkt.data[-3:] == TERMINATOR:
                self.eof = True
                pkt.data = pkt.data[:-3]

            #Write to file
            self.writer.write(pkt.data)

        else:
            print "PKT %d received out of order"%(pkt.seq_num)
            # print pkt

        #Generate ACK packet and send to the sender
        ack_pkt = Packet.build_ack_packet(self.Rn)
        print "Sent ACK %d"%(self.Rn)
        self.sock.sendto(ack_pkt.generate_udp_payload(),addr)


    def __del__(self):
        self.writer.close()
        self.sock.close()

    def discard_pkt(self):
        return random.random() < self.err_prob

if __name__ == "__main__":
    if len(sys.argv)<4:
        print "Usage:"
        print "%s <port> <file> <error-probability>"%(sys.argv[0])
        exit(-1)

    port = int(sys.argv[1])
    filenm = sys.argv[2]
    p = float(sys.argv[3])

    g=GBNrx(filenm,p,port)
    g.start()

    del g