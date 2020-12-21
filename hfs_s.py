from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import argparse
import base64
import ssl
import os

arg_parser = argparse.ArgumentParser(description='Create a simple read-only HTTP/S file server')
arg_parser.add_argument('--cert', help='Certificate file path, if not provided uses http')
arg_parser.add_argument('--user', help='username:password, like user1:mypass, ' 
    'or a file holds the username:password in each line if not provided uses no authentication')
arg_parser.add_argument('--path', help='Path to serve, if not provided uses the current folder')
arg_parser.add_argument('--port', help='Port to serve the server, default http:8080, default https:4443', type=int)
args=arg_parser.parse_args()

single_user_key = args.user
credentials_file = None
if single_user_key is not None and os.path.isfile(single_user_key):
    credentials_file = args.user
certifacate_path = args.cert

if args.path is not None:
    os.chdir(args.path)

class AuthHandler(SimpleHTTPRequestHandler):
    def check_user(self, auth_text):
        global single_user_key, credentials_file
        if credentials_file is None:
            return auth_text == 'Basic ' + base64.b64encode(single_user_key.encode('ascii')).decode('ascii')
        else:
            with open(credentials_file) as f:
                for credentials in f.readline():
                    if single_user_key == 'Basic ' + base64.b64encode(credentials.encode('ascii')).decode('ascii'):
                        return True
                return False

    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        print("send header")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print("send header")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write(b'no auth header received')
            pass
        elif self.check_user(self.headers.get('Authorization')):
            SimpleHTTPRequestHandler.do_GET(self)
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(str.encode(self.headers.get('Authorization')))
            self.wfile.write(b'\t!not authenticated\n')
            pass

if certifacate_path is not None:
    if single_user_key is not None:
        httpd = TCPServer(('', 4443 if args.port is None else args.port), AuthHandler)
    else:
        httpd = TCPServer(('', 4443 if args.port is None else args.port), SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket (httpd.socket, certfile=certifacate_path, server_side=True)
    sa = httpd.socket.getsockname()
    print("Serving HTTP on "+ str(sa[0])+ " port "+ str(sa[1])+ "...")
    httpd.serve_forever()
else:
    if single_user_key is not None:
        httpd = TCPServer(('', 8080 if args.port is None else args.port), AuthHandler)
    else:
        httpd = TCPServer(('', 8080 if args.port is None else args.port), SimpleHTTPRequestHandler)
    sa = httpd.socket.getsockname()
    print("Serving HTTP on "+ str(sa[0])+ " port "+ str(sa[1])+ "...")
    httpd.serve_forever()
