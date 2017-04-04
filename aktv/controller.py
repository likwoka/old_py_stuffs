'''
aktvcontroller - a client program using XMLRPC to control the server's app
                 (aktv).

Copyright (c) Alex Li 2003.  All rights reserved.

Example:
aktvcontroller 127.0.0.1 8000 start_app
aktvcontroller 127.0.0.1 8000 stop_app
aktvcontroller 127.0.0.1 8000 shutdown_server_program
aktvcontroller 127.0.0.1 8000 shutdown_machine
aktvcontroller 127.0.0.1 8000 restart_machine
'''
__VERSION__ = '0.1'
__AUTHOR__ = 'Alex Li <likwoka@yahoo.com>'

import sys
import socket
import xmlrpclib
from optparse import OptionParser

from aktv import xmlrpc

def parse_cmdline(argv):
    '''The command line parsing hook.  Customize this.
    Returns opts, args where both are tuples
    '''
    usage = 'usage: %prog [options] ip_addr port action optional_args'
    parser = OptionParser(usage=usage, version=__VERSION__)
    (opts, args) = parser.parse_args()
    
    if len(args) < 3: # must at least have ipaddr, port and action
        parser.error('Incorrect number of arguments')

    return (opts, args)


def logic(opts, args):
    '''The script logic hook.  Customize this.'''
    try:
        result = xmlrpc.make_xmlrpc_call(args[0], args[1], args[2], *args[3:])
    except socket.error, errmsg:
        msg = 'Server not found.  Probably wrong ip address or port.' \
              '  %s' % errmsg
        print msg
    except xmlrpclib.Fault, errmsg:
        msg = 'XMLRPC Error.  Probably a wrong action name.  ' \
              'From server: %s' % errmsg
        print msg
    else:
        print result 


def main(argv=None):
    if argv is None:
        argv = sys.argv
    (opts, args) = parse_cmdline(argv)
    logic(opts, args)
    

if __name__ == '__main__':
    sys.exit(main())
