from twisted.internet import defer, protocol, reactor
import sys


class ScanningProtocol(protocol.Protocol):
    def connectionMade(self):
        port = self.transport.getPeer().port
        self.factory.deferred.callback(port)
        self.transport.loseConnection()


class ScannerClientFactory(protocol.ClientFactory):
    protocol = ScanningProtocol

    def __init__(self):
        self.deferred = defer.Deferred()

    def clientConnectionFailed(self, connector, reason):
        self.deferred.errback(reason)


def connect(host, port):
    scanner = ScannerClientFactory()
    reactor.connectTCP(host, port, scanner)
    return scanner.deferred


def main(argv):
    if len(argv) != 4:
        print "Usage: portscan.py localhost 1 80"
        return 1

    host  = argv[1]
    start = int(argv[2])
    end   = int(argv[3])

    scan_results = [connect(host, port) for port in range(start, end+1)]

    def print_result(scan_results):
        for (success, result) in scan_results:
            if success:
                print "Connected to port %s" % result
        reactor.stop()

    dl = defer.DeferredList(scan_results, consumeErrors=True)
    dl.addCallback(print_result)

    reactor.run()

def time_test():
    from timeit import Timer
    t = Timer("main(sys.argv)", "from __main__ import main")
    print t.timeit(1)


if __name__ == "__main__":
    time_test()
    #main(sys.argv)
