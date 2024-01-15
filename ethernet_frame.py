import socket
import struct


class EthernetFrame:
    """
    Used to parse the Ethernet frame
    The raw_data is the data received from the socket and has the format:
    [Destination MAC][Source MAC][Protocol][Data]
    Where:
        Destination MAC: 6 bytes
        Source MAC: 6 bytes
        Protocol: 2 bytes
        Data: the rest of the packet
    """
    def __init__(self, raw_data):
        dest_mac, src_mac, protocol = struct.unpack('! 6s 6s H', raw_data[:14])
        self.address_destination_mac = EthernetFrame.get_mac_addr(dest_mac)
        self.address_source_mac = EthernetFrame.get_mac_addr(src_mac)
        self.protocol = socket.htons(protocol)
        self.data = raw_data[14:]

    """
    Converts the MAC address from bytes to the format AA:BB:CC:DD:EE:FF
    Args:
        bytes_addr (bytes): The MAC address in bytes
    Returns:
        mac_addr (str): The MAC address in the format AA:BB:CC:DD:EE:FF
    """
    @staticmethod
    def get_mac_addr(bytes_addr):
        bytes_str = map('{:02x}'.format, bytes_addr)
        return ':'.join(bytes_str).upper()