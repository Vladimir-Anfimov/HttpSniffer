import struct


class Ipv4Datagram:
    def __init__(self, ip_datagram):
        vihl, _, self.total_length, self.identification, flags_offset, _, self.protocol, _, src, dest = \
          struct.unpack('! B B H H H B B H 4s 4s', ip_datagram[:20])

        self.header_length = (vihl & 15) * 4

        self.dnf_flag = (flags_offset >> 14) & 1
        self.mff_flag = (flags_offset >> 13) & 1

        self.frag_offset = flags_offset & 8191

        self.src = Ipv4Datagram.get_ipv4_addr(src)
        self.dest = Ipv4Datagram.get_ipv4_addr(dest)

        self.data = ip_datagram[self.header_length:]
        
        
    @staticmethod
    def get_ipv4_addr(bytes_addr):  
        return '.'.join(map(str, bytes_addr))
    
    def __str__(self) -> str:
        return f"""IPv4 Datagram:
        Source: {self.src}, Target: {self.dest}
        Identification: {self.identification} Fragment Offset: {self.frag_offset}
        DNF Flag: {self.dnf_flag}, MFF Flag: {self.mff_flag}"""
