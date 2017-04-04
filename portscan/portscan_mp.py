"""
Thread-based message passing.
High-light:
-   No locks!
-   each thread cannot access other's data ... 
    communicate by calling send()
"""


import sys, threading, socket
from Queue import Queue

NUM_OF_WORKERS = 1000


class Base:
    def __init__(self):
        self._queue = Queue()
        self._t = threading.Thread(target=self.run)
        self._t.setDaemon(True)
        self._t.start()

    def send(self, message):
        self._queue.put(message)

    def receive(self):
        return self._queue.get()

    def run(self):
        pass

    def wait_for_finish(self):
        self._t.join()


class Scanner(Base):
    def __init__(self, collector):
        self._collector = collector
        Base.__init__(self)

    def run(self):
        while True:
            target = self.receive()
            can_connect = self.try_connect(target)
            self._collector.send((target.port, can_connect))

    def try_connect(self, target):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((target.host, target.port))
            return True
        except:
            return False
        finally:
            s.close()


class Collector(Base):
    def __init__(self, port_count):
        self._result = []
        self._count = 0
        self.port_count = port_count
        Base.__init__(self)

    def run(self):
        while True:
            (port, can_connect) = self.receive()
            self._count += 1
            if can_connect:
                self._result.append(port)

            if self._count == self.port_count:
                self._result.sort()
                for port in self._result:
                    print "Connected to port %s" % port
                return


class Target:
    def __init__(self, host, port):
        self.host = host
        self.port = port


def main(argv):
    if len(argv) != 4:
        print "Usage: portscan_mp.py localhost 1 80"
        return 1   
    
    host  = argv[1]
    start = int(argv[2])
    end   = int(argv[3])

    collector = Collector(end+1 - start)
    scanners = [Scanner(collector) for i in range(0, NUM_OF_WORKERS)]

    i = 0
    for port in range(start, end+1):
        scanners[i].send(Target(host, port))
        i += 1
        if i == NUM_OF_WORKERS:
            i = 0
    
    collector.wait_for_finish()
    return 0


def time_test():
    from timeit import Timer
    t = Timer("main(sys.argv)", "from __main__ import main")
    print t.timeit(1)
      

if __name__ == "__main__":
    time_test()
    #sys.exit(main(sys.argv))
