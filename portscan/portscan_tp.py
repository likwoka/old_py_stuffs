"""
A worker thread model implemented using a thread pool.
Highlight:
-   1 Queue (lock based)
-   Use RLock for results

Rough benchmark on Python 2.5, Pentium M 1.70GHz 1.0GB RAM
for scanning port 1 to 5000:

NUM_OF_WORKERS  Time (s)
1000              5.85
 500             11.91
 400             13.97
 300             17.79
 200             28.60
 100             50.27
  50            100.55


Twisted 2.50
   1             20.00
"""

import sys, threading, socket
from Queue import Queue

NUM_OF_WORKERS = 1000


class Target:
    def __init__(self, host, port):
        self.host = host
        self.port = port


class Results:
    def __init__(self):
        self._results = []
        self._lock = threading.RLock()

    def append(self, result):
        self._lock.acquire()
        self._results.append(result)
        self._lock.release()
        
    def print_result(self):
        for (port, can_connect) in self._results:
            if can_connect:
                print "Connected to port %s" % port


class Connector:
    def __init__(self, work_queue, results):
        self.work_queue = work_queue
        self.results = results

    def run(self):
        while True:
            target = self.work_queue.get()
            result = self.try_connect(target)
            self.results.append((target.port, result))
            self.work_queue.task_done()

    def try_connect(self, target):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((target.host, target.port))
            return True
        except:
            return False
        finally:
            s.close()


def main(argv):
    if len(argv) != 4:
        print "Usage: portscan_tp.py localhost 1 80"
        return 1
    
    host  = argv[1]
    start = int(argv[2])
    end   = int(argv[3])
    
    results = Results()

    work_queue = Queue()
    for port in range(start, end+1):
        work_queue.put(Target(host, port))

    connectors = []
    for i in range(NUM_OF_WORKERS):
        c = Connector(work_queue, results)
        t = threading.Thread(target=c.run)
        t.setDaemon(True)
        t.start()

    work_queue.join()
    results.print_result()
    return 0


def time_test():
    from timeit import Timer
    t = Timer("main(sys.argv)", "from __main__ import main")
    print t.timeit(1)


if __name__ == "__main__":
    time_test()
    #main(sys.argv)
