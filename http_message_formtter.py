from http_message import HttpMessage


class HttpMessageFormatter:
    def __init__(self, message: HttpMessage):
        self.message = message
        self.format = []
        self.build()

    def build(self):
        self.format.append(f"HTTP Message:")
        self.format.append(f"Src: {self.message.ip_src}:{self.message.port_src}")
        self.format.append(f"Dest: {self.message.ip_dest}:{self.message.port_dest}")
        self.format.append(f"Method: {self.message.method}, Path: {self.message.path}, Version: {self.message.version}")
        self.format.append(f"Headers: {self.message.headers}")
        self.format.append(f"Body: {self.message.body.decode('utf-8')}")

    
    def __str__(self) -> str:
        return "\n".join(self.format)
    

    def __iter__(self):
        return iter(self.format)