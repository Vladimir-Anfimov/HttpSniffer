import struct


class TcpSegment:
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