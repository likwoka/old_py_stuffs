"""
Cross-platform (posix/nt) API for flock-style file locking.

Synopsis:

   import portalocker
   file = open("somefile", "r+")
   portalocker.lock(file, portalocker.EX)
   file.seek(12)
   file.write("foo")
   file.close()

If you know what you're doing, you may choose to

   portalocker.unlock(file)

before closing the file, but why?

Methods:

   lock(file, flags)
   unlock(file)

Constants:

   EX -- Exclusive Lock
   SH -- Shared Lock
   NB -- Non-blocking Lock (fail immediately if blocked)

I learned the win32 technique for locking files from sample code
provided by John Nielsen <nielsenjf@my-deja.com> in the documentation
that accompanies the win32 modules.

Author: Jonathan Feinberg <jdf@pobox.com>
Version: $Id: portalocker.py,v 1.3 2001/05/29 18:47:55 Administrator Exp $
"""


import os


if os.name == 'nt':
    
    import win32con
    import win32file
    import pywintypes

    # is there any reason not to reuse the following structure?
    __overlapped = pywintypes.OVERLAPPED()
    
    EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    SH = 0 # the default
    NB = win32con.LOCKFILE_FAIL_IMMEDIATELY

    def lock(file, flags):
        hfile = win32file._get_osfhandle(file.fileno())
        # 0xffff0000 is -65536 for python < 2.4
        win32file.LockFileEx(hfile, flags, 0, -65536, __overlapped)

    def unlock(file):
        hfile = win32file._get_osfhandle(file.fileno())
        win32file.UnlockFileEx(hfile, 0, -65536, __overlapped)

elif os.name == 'posix':
    
    import fcntl
    
    EX = fcntl.LOCK_EX
    SH = fcntl.LOCK_SH
    NB = fcntl.LOCK_NB

    def lock(file, flags):
        fcntl.flock(file.fileno(), flags)

    def unlock(file):
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)

else:
    raise RuntimeError("PortaLocker only defined for nt and posix platforms")


if __name__ == '__main__':
    from time import time, strftime, localtime
    import sys
    import portalocker

    log = open('log.txt', "a+")
    portalock.lock(log, portalocker.LOCK_EX)

    timestamp = strftime("%m/%d/%Y %H:%M:%S\n", localtime(time()))
    log.write( timestamp )

    print "Wrote lines. Hit enter to release lock."
    dummy = sys.stdin.readline()

    log.close()

