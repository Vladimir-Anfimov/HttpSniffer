import socket

from ethernet_frame import EthernetFrame
from http_message_formtter import HttpMessageFormatter
from http_message_store import HttpMessageStore
from ipv4_datagram import Ipv4Datagram
from tcp_segment import TcpSegment
from http_message import HttpMessage

from threading import Thread

class HttpSniffer(Thread):
    PACKET_SIZE = 65535
    IP_PROTOCOL = 8
    HTTP_PORT = 80
    TCP_PROTOCOL = 6

    def __init__(self, http_message_store: HttpMessageStore):
        Thread.__init__(self)
        self.http_message_store = http_message_store

    def run(self):
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

        self.messages = []

        while True:
            raw_data, _ = s.recvfrom(HttpSniffer.PACKET_SIZE)
            ethernet_frame = EthernetFrame(raw_data)
           
            if ethernet_frame.protocol != HttpSniffer.IP_PROTOCOL:
                continue

            ipv4_datagram = Ipv4Datagram(ethernet_frame.data)
                
            if ipv4_datagram.protocol != HttpSniffer.TCP_PROTOCOL:
                continue

            tcp_segment = TcpSegment(ipv4_datagram.data)

            if HttpSniffer.HTTP_PORT not in [tcp_segment.src_port, tcp_segment.dest_port] or tcp_segment.data == b'':
                continue

            self.message_process(ipv4_datagram, tcp_segment)



    def message_process(self, ipv4_datagram: Ipv4Datagram, tcp_segment: TcpSegment):
        try:
            http_message = HttpMessage(
                tcp_segment.data,
                ipv4_datagram.src,
                ipv4_datagram.dest,
                tcp_segment.src_port,
                tcp_segment.dest_port)
            
            print(HttpMessageFormatter(http_message))
            self.http_message_store.add(http_message)
        except UnicodeDecodeError:
            print('\tHTTP Data: Unable to decode')

        print()