from multiprocessing import Process
from threading import Thread
import server
from http.server import BaseHTTPRequestHandler, HTTPServer
import gui

if __name__ == '__main__':
    webServer = HTTPServer(('localhost', 9080), server.HttpHandler)
    print('running http server: http://localhost:9080')  # some consoles will display URL as clickable so it is easier to run browser
    t = Thread(target=webServer.serve_forever, daemon=True)
    t.start()
    
    Gui = gui.gui()
    Gui.gui_main()
