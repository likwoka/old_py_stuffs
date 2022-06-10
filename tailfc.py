#!/usr/bin/env python

import os, time, sys

def tailf(path, cr):
    f = open(path)
    f.seek(0, os.SEEK_END)
    while 1:
        line = f.readline()
        if len(line) > 0:
            cr.send(line)
        else:
            time.sleep(1) # 1 sec

def cprint():
    while 1:
        line = (yield)
        print(line)

if __name__ == "__main__":
    path = sys.argv[1]
    p = cprint()
    p.next()
    tailf(path, p)