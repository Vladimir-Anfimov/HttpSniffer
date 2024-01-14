import socket

from ethernet_frame import EthernetFrame
from ipv4_datagram import Ipv4Datagram
from tcp_segment import TcpSegment
from colorama import Fore, Style

class HttpSniffer:
    PACKET_SIZE = 65535
    IP_PROTOCOL = 8
    HTTP_PORT = 80
    TCP_PROTOCOL = 6

    def run(self):
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        

        while True:
            raw_data, _ = s.recvfrom(HttpSniffer.PACKET_SIZE)
            ethernet_frame = EthernetFrame(raw_data)
           
            if ethernet_frame.protocol != HttpSniffer.IP_PROTOCOL:
                continue

            ipv4_datagram = Ipv4Datagram(ethernet_frame.data)
                
            if ipv4_datagram.protocol != HttpSniffer.TCP_PROTOCOL:
                continue

            tcp_segment = TcpSegment(ipv4_datagram.data)


            if HttpSniffer.HTTP_PORT not in [tcp_segment.src_port, tcp_segment.dest_port]:
                continue

           
            self.packet_manager(ipv4_datagram, tcp_segment)



    def packet_manager(self, ipv4_datagram: Ipv4Datagram, tcp_segment: TcpSegment):
        print(str(ipv4_datagram), '\n', str(tcp_segment), '\n')

        try:
            http = tcp_segment.data.decode('utf-8', errors='replace')
            print(f'\tHTTP Data: {Fore.GREEN}{http}{Style.RESET_ALL}')

        except UnicodeDecodeError:
            print('\tHTTP Data: Unable to decode')

        print()