import http.server
import socketserver
import threading
import os

PORT = 80
PATH = './webserver/'

def start_server(path, port=80):
    #Path variable not implermented
    os.chdir(path)

    httpd = http.server.HTTPServer(('', port), http.server.CGIHTTPRequestHandler)
    httpd.serve_forever()

daemon = threading.Thread(name='daemon_server', target=start_server, args=(PATH, PORT))
daemon.setDaemon(True)
daemon.start()

print('Web Server Running...')

while True:
    pass
