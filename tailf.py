#!/usr/bin/env python

import os, time, sys

def tailf(path):
    f = open(path)
    f.seek(0, os.SEEK_END)
    while 1:
        line = f.readline()
        if len(line) > 0:
            yield line
        else:
            time.sleep(1) # 1 sec


if __name__ == "__main__":
    path = sys.argv[1]
    for line in tailf(path):
        print line

