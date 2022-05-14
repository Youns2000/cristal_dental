import random
import json
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
        if self.path != "/keygen":
                self.send_response(404)
                content = "not found"
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
                return
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<body>", "utf-8"))
        with open('json_data.json', 'w') as outfile:
            json.dump(key_gen(), outfile)
        self.wfile.write(bytes("<p>Key generated!</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))