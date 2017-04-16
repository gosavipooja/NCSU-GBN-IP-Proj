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
    print(s.getsockname()[0])
    s.close()