import struct


class Ipv4Datagram:
    """
    Used to parse the IPv4 datagram
    The ip_datagram is extracted from the Ethernet frame and has the format:
    [Version][IHL][_][Total Length][Identification][Flags][Fragment Offset][_][Protocol][_][Source Address][Destination Address][_][_][Data]
    Where:
        Version: 4 bits
        IHL: 4 bits (It is the number of 32-bit words in the header and must be multiplied by 4 to get the header length)
        Total Length: 16 bits
        Identification: 16 bits
        Flags: 3 bits (The first bit is always 0, the second bit is the DNF flag, and the third bit is the MFF flag)
        Fragment Offset: 13 bits
        Protocol: 8 bits
        Source Address: 32 bits
        Destination Address: 32 bits
        Data: the rest of the packet
    """
    def __init__(self, ip_datagram):
        vihl, _, self.total_length, self.identification, flags_offset, _, self.protocol, _, src, dest = \
          struct.unpack('! B B H H H B B H 4s 4s', ip_datagram[:20])

        self.header_length = (vihl & 15) * 4

        self.dnf_flag = (flags_offset >> 14) & 1
        self.mff_flag = (flags_offset >> 13) & 1

        self.frag_offset = flags_offset & 8191 # 8191 = 2^13 - 1, so we get the last 13 bits

        self.src = Ipv4Datagram.get_ipv4_addr(src)
        self.dest = Ipv4Datagram.get_ipv4_addr(dest)

        self.data = ip_datagram[self.header_length:]
        

    """
    Converts the IPv4 address from bytes to the format A.B.C.D, where A, B, C and D are integers between 0 and 255
    Args:
        bytes_addr (bytes): The IPv4 address in bytes
    Returns:
        ipv4_addr (str): The IPv4 address in the format A.B.C.D
    """   
    @staticmethod
    def get_ipv4_addr(bytes_addr):  
        return '.'.join(map(str, bytes_addr))
    

    def __str__(self) -> str:
        return f"""IPv4 Datagram:
        Source: {self.src}, Target: {self.dest}
        Identification: {self.identification} Fragment Offset: {self.frag_offset}
        DNF Flag: {self.dnf_flag}, MFF Flag: {self.mff_flag}"""
