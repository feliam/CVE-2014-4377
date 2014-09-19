#!/usr/bin/env python
# Runs a small cgi server.

import CGIHTTPServer
import SimpleHTTPServer
import BaseHTTPServer
import SocketServer

class MyRequestHandler( CGIHTTPServer.CGIHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Pragma", "no-cache")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        CGIHTTPServer.CGIHTTPRequestHandler.end_headers(self)



print  SimpleHTTPServer.__version__
HandlerClass = MyRequestHandler
ServerClass = BaseHTTPServer.HTTPServer
BaseHTTPServer.test(HandlerClass, ServerClass)
