import struct


class TcpSegment:
    """
    Used to parse the TCP segment
    The data is extracted from the IPv4 datagram and has the format:
    [Source Port][Destination Port][Sequence Number][Acknowledgement Number][Offset][_][Flags][_][_][_][_][_][Data]
    Where:
        Source Port: 16 bits
        Destination Port: 16 bits
        Sequence Number: 32 bits
        Acknowledgement Number: 32 bits
        Offset: 4 bits (It is the number of 32-bit words in the header and must be multiplied by 4 to get the header length)
        Flags: 9 bits (The first bit is the FIN flag, the second bit is the SYN flag, and the third bit is the ACK flag)
        Data: the rest of the packet 
    """
    def __init__(self, data):
        self.src_port, self.dest_port, self.seq_number, self.ack_number, offset_reserved_flags = struct.unpack('! H H L L H', data[:14])
        offset = (offset_reserved_flags >> 12) * 4
        self.ack_flag = (offset_reserved_flags >> 4) & 1
        self.syn_flag = (offset_reserved_flags >> 1) & 1
        self.fin_flag = offset_reserved_flags & 1

        self.data = data[offset:]


    def __str__(self) -> str:
        return f"""TCP Segment:
        Source Port: {self.src_port}, Destination Port: {self.dest_port} 
        Sequence Number: {self.seq_number} Acknowledgement Number: {self.ack_number}
        ACK Flag: {self.ack_flag}, SYN Flag: {self.syn_flag}, FIN Flag: {self.fin_flag}"""