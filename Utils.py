import hashlib
import socket

def generate_chksum(data):
    m = hashlib.md5()
    m.update(data)
    return int(m.hexdigest()[:4],16)

#Converts a number to byte array where the array length is n/8
#largest byte is first
def int_to_byte_array(x, n):
    val = []
    for i in range(n/8):
        val.insert(0,x & 0xFF)
        x = x>>8
    return val

def byte_array_to_int(b_arr):
    val = 0
    for b in b_arr:
        val = (val << 8) + ord(b)
    return val

def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    val = s.getsockname()[0]
    s.close()
    return val

# From stackoverflow: http://stackoverflow.com/questions/3949726/calculate-ip-checksum-in-python
def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    #zero padding
    if(len(msg)%2==1):
        msg = msg + '\x00'
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff


# msg = "hello"
# print "0x%X"%checksum(msg)