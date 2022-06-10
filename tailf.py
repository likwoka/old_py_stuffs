#!/usr/bin/env python
'''
tailf.py -- doing tail(1) -f in python
ex: 
    tailf.py /path/to/logfile           # show new lines
    tailf.py /path/to/logfile -n 10     # show the last 10 lines first before new lines
    tailf.py /path/to/logfile -n        # show the whole file, then new lines
'''
import os, time, sys

def tailf(path, has_n, num_lines):
    '''tailf is a generator function that returns the line in the
    file through iteration.
    '''
    f = open(path)
    if has_n:
        if num_lines <= 0:
            f.seek(0, os.SEEK_SET)
        else:
            # TODO
            pos = find_pos(f, num_lines)
            f.seek(pos, os.SEEK_END)
    else:
        f.seek(0, os.SEEK_END)
    while 1:
        line = f.readline()
        if len(line) > 0:
            yield line
        else:
            time.sleep(1) # 1 sec

def find_pos(f, num_lines):
    BUFSIZE = 1024
    f.seek(0, os.SEEK_END)
    bytes = f.tell()
    size = num_lines
    block = -1
    data = ''
    current_pos = -bytes

    while size > 0 and bytes > 0:
        if (bytes - BUFSIZE < 0):
            # file too small, start from begining
            return 0
        else:
            # Seek back one whole BUFSIZE
            f.seek(block*BUFSIZE, os.SEEK_END)
            # read BUFFER
            data = f.read(BUFSIZE)
        linesFound = data.count('\n')
        size -= linesFound
        bytes -= BUFSIZ
        block -= 1    
    return 0


def is_int(val):
    '''is_int returns True if val is an integer,
    False otherwise.
    '''
    try:
        int(val)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    argv = sys.argv
    path = argv[1]
    has_n = False
    num_lines = 0

    # with tailf.py logfile -n X
    if len(argv) == 3 and argv[2] == '-n':
        has_n = True
        num_lines = 0
    elif len(argv) == 4 and argv[2] == '-n' and is_int(argv[3]):
        has_n = True
        num_lines = int(argv[3])

    for line in tailf(path, has_n, num_lines):
        print line
