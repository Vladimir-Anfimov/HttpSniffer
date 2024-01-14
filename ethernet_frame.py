import socket
import struct


class EthernetFrame:
    def __init__(self, raw_data):
        dest_mac, src_mac, protocol = struct.unpack('! 6s 6s H', raw_data[:14])
        self.address_destination_mac = EthernetFrame.get_mac_addr(dest_mac)
        self.address_source_mac = EthernetFrame.get_mac_addr(src_mac)
        self.protocol = socket.htons(protocol)
        self.data = raw_data[14:]

    @staticmethod
    def get_mac_addr(bytes_addr):
        bytes_str = map('{:02x}'.format, bytes_addr)
        return ':'.join(bytes_str).upper()