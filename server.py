import random
from http.server import BaseHTTPRequestHandler, HTTPServer

def key_gen():
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    key = ""
    i = 0
    for i in range(5):
        for j in range(4):
            key += random.choice(alphabet)
        if i < 4:
            key += "-"
    return key

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))