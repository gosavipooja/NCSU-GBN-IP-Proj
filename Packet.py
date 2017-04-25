from Utils import *
from Constants import *
import array

class Packet:
    num_pkts = 0

    def __init__(self,data = None):
        if data is not None:
            self.seq_num = Packet.num_pkts
            Packet.num_pkts = Packet.num_pkts + 1
            self.data = data
            # self.checksum = generate_chksum(data)
            self.checksum = checksum(data)
            self.indicator = DATA_PKT_IDENTIFIER


    def valid_checksum(self):
        # computed_chksum = generate_chksum(self.data)
        computed_chksum = checksum(self.data)
        return computed_chksum==self.checksum

    def generate_udp_payload(self):
        payload = bytearray('')
        payload.extend(int_to_byte_array(self.seq_num, 32))
        payload.extend(int_to_byte_array(self.checksum, 16))
        payload.extend(int_to_byte_array(self.indicator, 16))
        payload.extend(self.data)
        return  str(payload)

    @classmethod
    def build_packet(cls,s,is_ack=False):
        p = Packet(None)
        p.seq_num = byte_array_to_int(s[SEQ_OFFSET:SEQ_OFFSET+SEQ_LEN])
        p.checksum = byte_array_to_int(s[CHKSUM_OFFSET:CHKSUM_OFFSET+CHKSUM_LEN])
        p.indicator = byte_array_to_int(s[DATAID_OFFSET:DATAID_OFFSET+DATAID_LEN])
        if not is_ack:
            p.data = s[DATA_OFFSET:]
        return p

    @classmethod
    def build_ack_packet(cls,n):
        p = Packet(None)
        p.seq_num = n
        p.checksum = 0
        p.indicator = DATA_PKT_IDENTIFIER
        p.data = ''
        return p

    def __str__(self):
        s = "Seq No = %d\t" \
            "CHKSUM = %X\t" \
            "Data Indicator = 0x%X\n" \
            "Data = %s"%(self.seq_num,self.checksum,self.indicator,self.data)
        # return str(self.data)
        return s

