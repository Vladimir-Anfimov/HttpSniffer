from tcp_segment import TcpSegment


class HttpMessage:
    def __init__(self, data, ip_src, ip_dest, port_src, port_dest):
        self.ip_src = ip_src
        self.ip_dest = ip_dest

        self.port_src = port_src
        self.port_dest = port_dest

        self.method = None
        self.path = None
        self.version = None
        self.headers = {}
      

        if b'\r\n\r\n' in data:
            headers, body = data.split(b'\r\n\r\n', 1)
        else:
            headers = data
            body = b''

        self.body = body
        self.parse_headers(headers)


    def parse_headers(self, headers):
        headers = headers.split(b'\r\n')
        self.parse_request_line(headers[0])
        self.parse_headers_lines(headers[1:])


    def parse_request_line(self, request_line):
        try:
            method, path, version = request_line.split(b' ')
            self.method = method.decode('utf-8')
            self.path = path.decode('utf-8')
            self.version = version.decode('utf-8')
        except Exception:
            pass


    def parse_headers_lines(self, headers_lines):
        self.headers = {}
        for header_line in headers_lines:
            header, value = header_line.split(b': ')
            self.headers[header.decode('utf-8')] = value.decode('utf-8')



    def __str__(self):
        return f"""HTTP Message:
        Source: {self.ip_src}:{self.port_src}
        Destination: {self.ip_dest}:{self.port_dest}
        Method: {self.method}, Path: {self.path}, Version: {self.version}
        Headers: {self.headers}
        Body: {self.body.decode('utf-8')}
        """
    