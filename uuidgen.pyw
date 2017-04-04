"""
Generate a bunch of Version-4 UUIDs.

Requirement:
    Python 2.5+, Windows Notepad.
"""

VERSION = "0.1"
NUM_TO_GENERATE = 20

import uuid, tempfile, os

uuids = []
for i in xrange(0, NUM_TO_GENERATE):
    uuids.append(str(uuid.uuid4()).upper())

(fd, path) = tempfile.mkstemp(suffix=".txt")
newline = os.linesep

f = os.fdopen(fd, "w+b")
f.write(newline.join(uuids))
f.close()

# We are doing this instead of a simple
# os.startfile(path) so that we can delete 
# the file when the notepad is closed.
import subprocess, atexit
atexit.register(os.remove, path)
subprocess.call(["notepad", path])
