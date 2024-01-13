from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, World!')

def run_server():
    server_address = ('', 80)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print('Server running on http://localhost:80')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
