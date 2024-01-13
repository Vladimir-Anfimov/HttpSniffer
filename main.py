import socket
import struct


def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()


def get_ipv4_addr(bytes_addr):  
    return '.'.join(map(str, bytes_addr))


def ethernet_frame(raw_data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', raw_data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), raw_data[14:]


def ipv4_packet(data):
    version_header_length = data[0]
    header_length = (version_header_length & 15) * 4
    _, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return header_length, proto, get_ipv4_addr(src), get_ipv4_addr(target), data[header_length:]


def tcp_packet(data):
    src_port, dest_port, _, _, offset_reserved_flags = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserved_flags >> 12) * 4

    return src_port, dest_port, data[offset:]

def main():
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    while True:
        raw_data, _ = s.recvfrom(65535)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)


        # 8 for IPv4
        if eth_proto == 8:
            (header_length, proto, src, target, data) = ipv4_packet(data)
            # TCP
            if proto == 6:
                (src_port, dest_port, data) = tcp_packet(data)
                # print('\nEthernet Frame:')
                # print('Destination: {}, Source: {}, Protocol: {}'.format(dest_mac, src_mac, eth_proto))

                if src_port != 80 and dest_port != 80 or not b'HTTP' in data:
                    continue

                print('IPv4 Packet:')
                print('Header Length: {}, Protocol: {}, Source: {}, Target: {}'.format(header_length, proto, src, target))

                print('\tTCP Segment:')
                print('\tSource Port: {}, Destination Port: {}'.format(src_port, dest_port))

                try:
                    http = data.decode('utf-8')
                    print(f'\t\tHTTP Data: {http}\n')

                except UnicodeDecodeError:
                    print()

main()