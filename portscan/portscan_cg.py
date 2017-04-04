"""
candygram experiment --

My thought ... very attractive and simple style, but
the implementation is bad in the sense of weird syntax and
multiple ways of doing the same thing; and the error 
handling/reporting is almost non-existent...

Conclusion: Nice style, bad implementation
"""

import candygram as cg
import sys, socket


NUM_OF_WORKERS = 10


class Target:
    def __init__(self, host, port):
        self.host = host
        self.port = port


class Result:
    def __init__(self, port, is_success):
        self.port = port
        self.is_success = is_success
                      

def try_connect((collector, target)):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((target.host, target.port))
        can_connect = True
    except:
        can_connect = False
    finally:
        s.close()
    collector | Result(target.port, can_connect)


def scan():
    r = cg.Receiver()
    r[(cg.Process, Target)] = try_connect, cg.Message
    while 1:
        r.receive()


def main(argv):
    if len(argv) != 4:
        print "Usage: portscan_cg.py localhost 1 80"
        return 1   
    
    host  = argv[1]
    start = int(argv[2])
    end   = int(argv[3])

    r = cg.Receiver()
    r[Result] = lambda m : m, cg.Message

    scanners = [cg.spawn(scan) for i in range(0, NUM_OF_WORKERS)]

    i = 0
    for port in range(start, end+1):
        scanners[i] | (cg.self(), Target(host, port))
        i += 1
        if i == NUM_OF_WORKERS:
            i = 0

    port_count = end - start+1
    ports = []
    j = 0
    while j != port_count:
        result = r.receive()
        j += 1
        if result.is_success:
            ports.append(result.port)

    ports.sort()
    for port in ports:
        print "Connected to port %s" % port

    return 0


def time_test():
    from timeit import Timer
    t = Timer("main(sys.argv)", "from __main__ import main")
    print t.timeit(1)
      

if __name__ == "__main__":
    time_test()
    #sys.exit(main(sys.argv))

