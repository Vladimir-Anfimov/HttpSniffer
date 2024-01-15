import socket

from ethernet_frame import EthernetFrame
from http_message_formtter import HttpMessageFormatter
from http_message_store import HttpMessageStore
from ipv4_datagram import Ipv4Datagram
from tcp_segment import TcpSegment
from http_message import HttpMessage

from threading import Thread

class HttpSniffer(Thread):
    """
    Used to sniff the network for HTTP messages.
    """

    PACKET_SIZE = 65535
    IP_PROTOCOL = 8
    HTTP_PORT = 80
    TCP_PROTOCOL = 6


    """
    Initializes the HttpSniffer and executes the run method in a separate thread.
    Parameters:
        http_message_store (HttpMessageStore): The store to add the messages to.
    """
    def __init__(self, http_message_store: HttpMessageStore):
        Thread.__init__(self)
        self.http_message_store = http_message_store


    """
    Creates a socket to sniff the network.
    AF_PACKET: Address Family Packet that allows interaction with the network interface.
    SOCK_RAW: Socket type that allows to send and receive raw packets at a low level.
    socket.ntohs(3): The protocol to capture any type of packet from the network interface.
    """
    def get_socket(self):
        return socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))



    """
    The main loop of the sniffer.
    It receives the raw data from the socket and parses it.
    First it parses the Ethernet frame, then the IPv4 datagram, and finally the TCP segment.
    Calls the message_process method to process the HTTP message.
    """
    def run(self):
        s = self.get_socket()

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



    """
    It creates an HttpMessage object and adds it to the HttpMessageStore.
    Args:
        ipv4_datagram (Ipv4Datagram): The IPv4 datagram
        tcp_segment (TcpSegment): The TCP segment
    """
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