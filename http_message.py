class HttpMessage:
    """
    Used to parse and extract the HTTP message
    The data is extracted from the TCP segment and has the format:
    [Request Line][Headers][Body]
    Where:
        Request Line: [Method][Path][Version]
        Headers: array of [Header][Value]
        Body: the rest of the packet

    It also extracts the source and destination IP addresses and ports from the TCP segment.
    """
    def __init__(self, data, ip_src, ip_dest, port_src, port_dest):
        self.ip_src = ip_src
        self.ip_dest = ip_dest

        self.port_src = port_src
        self.port_dest = port_dest

        self.method = None
        self.path = None
        self.version = None
        self.headers = {}
        
        self.parse_data(data)

        
    """
    The http message might be split into multiple TCP segments.
    This method splits the data into the headers and the body.
    Args:
        data (bytes): The data from the TCP segment
    """
    def parse_data(self, data):
        if b'\r\n\r\n' in data:
            headers, body = data.split(b'\r\n\r\n', 1)
        else:
            headers = data
            body = b''

        self.body = body
        self.parse_headers(headers)


    """
    Parses the headers and extracts the request line and the headers lines.
    Args:
        headers (bytes): The headers 
    """
    def parse_headers(self, headers):
        headers = headers.split(b'\r\n')
        self.parse_request_line(headers[0])
        self.parse_headers_lines(headers[1:])


    """
    Parses the request line and extracts the method, path and version.
    Args:
        request_line (bytes): The request line 
    """
    def parse_request_line(self, request_line):
        try:
            method, path, version = request_line.split(b' ')
            self.method = method.decode('utf-8')
            self.path = path.decode('utf-8')
            self.version = version.decode('utf-8')
        except Exception:
            pass


    """
    Parses the headers lines and extracts the headers and their values.
    Args:
        headers_lines (bytes): The headers lines 
    """
    def parse_headers_lines(self, headers_lines):
        self.headers = {}
        for header_line in headers_lines:
            header, value = header_line.split(b': ')
            self.headers[header.decode('utf-8')] = value.decode('utf-8')
