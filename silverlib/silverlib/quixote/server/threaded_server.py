from quixote.server.simple_server import HTTPRequestHandler

from BaseHTTPServer import HTTPServer
from SocketServer import ThreadingMixIn



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = False



def run(create_publisher, host='', port=80, https=False):
    """
    Runs a simple, multi-threaded, synchronous HTTP server that
    publishes a Quixote application.
    """
    if https:
        HTTPRequestHandler.required_cgi_environment['HTTPS'] = 'on'
    httpd = ThreadedHTTPServer((host, port), HTTPRequestHandler)
    publisher = create_publisher()
    httpd.serve_forever()


if __name__ == '__main__':
    from quixote.server.util import get_server_parser
    parser = get_server_parser(run.__doc__)
    parser.add_option(
        '--https', dest="https", default=False, action="store_true",
        help=("Force the scheme for all requests to be https.  "
              "Not that this is for running the simple server "
              "through a proxy or tunnel that provides real SSL "
              "support.  The simple server itself does not. "))
    (options, args) = parser.parse_args()
    run(import_object(options.factory), host=options.host, port=options.port,
        https=options.https)
