from Packet import Packet
import socket
from Constants import *

rx_port = 7735
rx_ip = '127.0.0.1'

my_ip = '127.0.0.1'
my_port = 7000


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((my_ip,my_port))

# p0 = Packet('Hello')
# p1 = Packet(' World')
#
# s0 = p0.generate_udp_payload()
# s1 = p1.generate_udp_payload()


with open('RFC 882.txt','r') as f:
    while True:
        s = f.read(512)
        #print s
        p = Packet(s)
        sock.sendto(p.generate_udp_payload(),(rx_ip,rx_port))
        del p
        if(len(s)<512):
            end_p = Packet(TERMINATOR)
            sock.sendto(end_p, (rx_ip, rx_port))
            break