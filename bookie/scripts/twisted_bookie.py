#!/usr/bin/env python

"""
Single threaded asynchronous webserver.  Very good performance
and scalable (performance will degrade nicely).  Extremely 
resource (CPU, RAM) efficient.
"""

from quixote.server import twisted_server
from bookie import startup

startup.run(twisted_server.run, "quixote.conf", "bookie.conf")

