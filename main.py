from threading import Thread
import server
from http.server import BaseHTTPRequestHandler, HTTPServer
import gui

if __name__ == '__main__':
    webServer = HTTPServer(('localhost', 9080), server.HttpHandler)
    print('running http server: http://localhost:9080')
    t = Thread(target=webServer.serve_forever, daemon=True)
    t.start()

    gui.gui().start()
