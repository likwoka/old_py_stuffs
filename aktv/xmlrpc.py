from SimpleXMLRPCServer import SimpleXMLRPCServer
from threading import Event
import xmlrpclib
import socket


class XMLRPCServer(SimpleXMLRPCServer):
    '''I am an enhanced SimpleXMLRPCServer with:
    1) simple access control
    2) port rebinding
    3) server to be killed remotely (for clean shutdown)
    '''
    def __init__(self, server_ip, server_access_only, access_list, *args):
        SimpleXMLRPCServer.__init__(self, (args[0], args[1]))
        self._server_ip = server_ip
        self._server_access_only = server_access_only
        self._access_list = access_list
        self._listen_event = Event()
        
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SimpleXMLRPCServer.server_bind(self)

    def verify_request(self,request, client_address):
        if self._server_access_only:
            if client_address[0] == self._server_ip:
                return 1
            else:
                return 0
        else:
            if client_address[0] == self._server_ip or \
                client_address[0] in self._access_list:
                return 1
            else:
                return 0
        
    def serve_forever(self):
        self._listen_event.set()
        while self._listen_event.isSet():
            self.handle_request()

    def stop(self):
        self._listen_event.clear()

def make_xmlrpc_call(ipaddr, port, action, *args):
    '''Makes an XMLRPC call to a XMLRPC Server.'''
    server = xmlrpclib.ServerProxy('http://%s:%s' % (ipaddr, port))
    callstr = 'server.'
    if len(args) > 0: # not empty, therefore have arguments
        callstr += action + '(*args)'
    else: # no arguments
        callstr += action + '()'
    return eval(callstr, locals())

