import http.server
import socketserver

from functools import partial

import os
import sys
os.chdir(sys.path[0])


PORT = 8080
handler = partial(http.server.SimpleHTTPRequestHandler, directory="./menu")

with socketserver.TCPServer(("", PORT), handler) as http_server:
    print(os.getcwd())
    print(http_server.server_address)
    http_server.serve_forever()
