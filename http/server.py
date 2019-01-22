#!/usr/bin/python3
import os
import cgi
import urllib
from http.server import HTTPServer, CGIHTTPRequestHandler

class Handler(CGIHTTPRequestHandler):
    cgi_directories = ['/']

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['Content-Length'])
            postvars = urllib.parse.parse_qs(self.rfile.read(length),
                    keep_blank_values=1)
            if b'i' in postvars:
                loc = self.path + '/' + postvars[b'i'][0].decode("utf-8")
                self.send_response(302)
                self.send_header('Location', loc)
                self.end_headers()
                return
        super.do_POST()

    def is_cgi(self):
        request = self.path.split('?')
        if len(request) == 2:
            path, args = request
        else:
            path, args = request, None

        if isinstance(path, list):
            path = path[0]

        keywords = ['/source', '/ident', '/search']
        if any(k in path for k in keywords):
            os.environ["SCRIPT_URL"] = path
            self.cgi_info = '', 'web.py'
            return True
        elif path == '/':
            os.environ["SCRIPT_URL"] = '/linux/latest/source'
            self.cgi_info = '', 'web.py'
            return True
        return False

PORT = 8443

if "LXR_PROJ_DIR" not in os.environ:
    os.environ["LXR_PROJ_DIR"] = "/usr/local/share/elixir"
httpd = HTTPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
