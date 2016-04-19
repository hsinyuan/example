#/usr/bin/python
import sys
import urlparse
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler

class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        response_message = ""
        path = self.path
        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
            func_name = qs['callback'][0]
            value = qs['message'][0]
            response_message = "%s({\"message\":\"%s\"})" % (func_name,value)

        # Send the html message
        self.wfile.write(response_message)
        return


ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8000
server_address = ('127.0.0.1', port)

myHandler.protocol_version = Protocol
httpd = ServerClass(server_address, myHandler)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
