from http.server import HTTPServer, BaseHTTPRequestHandler, CGIHTTPRequestHandler
import socketserver
import threading
import os
from io import BytesIO

PORT = 80
PATH = './webserver/'

class SimpleHTTPRequestHandler(CGIHTTPRequestHandler):

    '''
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')
        
    '''
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        print("Content Length: " + str(content_length))
        body = self.rfile.read(content_length)
        print("Before-decoding: " + str(body))
        body = body.decode("utf-8")
        print("After-decoding: " + body)
        self.send_response(200)
        self.end_headers()

'''
Start server in the current thread. Is blocking
'''
def start_server(path = PATH, port=PORT):
    #Path variable not implermented
    os.chdir(path)

    httpd = HTTPServer(('', port), SimpleHTTPRequestHandler)
    httpd.serve_forever()

'''
Start server in a separate thread, and return that thread as an object.
'''
def start_server_thread(path = PATH, port = PORT):

    daemon = threading.Thread(name='daemon_server', target=start_server, args=(PATH, PORT))
    daemon.setDaemon(True)
    daemon.start()

    print('Web Server Running...')

    return daemon