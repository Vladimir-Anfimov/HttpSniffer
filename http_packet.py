
from dataclasses import dataclass


@dataclass
class HttpPacketContent:
    ip_src: str
    ip_dest: str
    port_src: int
    port_dest: int

    method: str
    url: str
    version: str
    headers: dict
    body: str

# GET / HTTP/1.1
# Host: localhost
# Connection: keep-alive
# Cache-Control: max-age=0
# sec-ch-ua: "Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "Linux"
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
# Sec-GPC: 1
# Accept-Language: en-US,en
# Sec-Fetch-Site: none
# Sec-Fetch-Mode: navigate
# Sec-Fetch-User: ?1
# Sec-Fetch-Dest: document
# Accept-Encoding: gzip, deflate, br

class HttpPacketBuilder:
    METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE']

    @staticmethod
    def build(ip_src, ip_dest, port_src, port_dest, raw_http_packet: bytes) -> HttpPacketContent:
        http_packet = HttpPacketBuilder()
        http_packet.ip_src = ip_src
        http_packet.ip_dest = ip_dest
        http_packet.port_src = port_src
        http_packet.port_dest = port_dest

    @staticmethod
    def _parse_method(raw_http_packet: bytes) -> str:
        for method in HttpPacketBuilder.METHODS:
            if raw_http_packet.startswith(method.encode()):
                return method
            
    @staticmethod
    def _parse_url(raw_http_packet: bytes) -> str:
        pass


