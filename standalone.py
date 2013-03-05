#!/usr/bin/env python

DEFAULT_PORT_NUMBER = 8080

def run_server(port = DEFAULT_PORT_NUMBER):
    from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer


    class HTTPHandler(BaseHTTPRequestHandler):

            def do_GET(self):
                import imp
                import re
                render = imp.load_source("render","render.cgi")
                id = None
                category = None
                match = re.findall(r"id\s*=\s*(\d*)",self.path)
                if match:
                    id = match[0]
                match = re.findall(r"cat\s*=\s*([^\s\;\&]*)",self.path)
                if match:
                    category = match[0]
                sys.stdout = self.wfile
                self.send_response(200)
                render.render_rst(id,category)
                return

    try:
            server = HTTPServer(('', port), HTTPHandler)
            print('Webserver is running on port %d' % port)
            server.serve_forever()

    except KeyboardInterrupt:
            print("Closing webserver ...")
            server.socket.close()
            print("Done")

def print_usage():
    print("Runs a standalone HTTP server for testing the blog system.")
    print("")
    print("Usage: standalone.py [-p PORT]")
    print("-p, --port PORT\tSpecify a port to be used. Default: {0}".format(DEFAULT_PORT_NUMBER))

if __name__ == "__main__":
    import getopt
    from sys import argv
    
    import sys,os
    os.chdir("cgi-bin")
    sys.path.append(os.getcwd())

    port = DEFAULT_PORT_NUMBER

    short_opts = "hp:"
    long_opts = ["help","p="]
    
    (opts,args) = getopt.getopt(argv[1:],short_opts,long_opts)
    
    for (opt,optarg) in opts:
        while opt[0] == '-':
            opt = opt[1:]
        if opt in ["h", "help"]:
            print_usage()
            exit(0)
        elif opt == 'p':
            port = int(optarg)
        else:
            print("Unknown option: '%s'" % opt)
        
    run_server(port)
