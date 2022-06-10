#!/usr/bin/env python
"""
Usage:
    sha1sum.py -h
    sha1sum.py /path/to/file

Output the sha1 checksum of the given file.

Options:
    -h, --help
"""

import sys, hashlib

class UsageError(Exception):
    def __init__(self, msg=""):
        super().__init__(msg)

def main():
    try:
        if len(sys.argv) != 2:
            raise UsageError(__doc__)

        filepath = sys.argv[1]
        with open(filepath, 'rb') as f:
            content = f.read()

        hobj = hashlib.sha1(content)
        print(hobj.hexdigest())
        return 0
    except Exception as err:
        print(err)
        return 1


if __name__ == "__main__":
    sys.exit(main())
