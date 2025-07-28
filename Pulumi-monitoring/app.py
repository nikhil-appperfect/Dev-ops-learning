from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server, Counter

# Define a metric
HELLO_REQUESTS = Counter('hello_requests_total', 'Total number of hello requests')

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            HELLO_REQUESTS.inc()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Hello, Prometheus!\n")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    # Start HTTP server for app on port 8080
    server = HTTPServer(('', 8080), HelloHandler)
    print("Serving on port 8080 and exposing metrics on 8000")
    server.serve_forever()
