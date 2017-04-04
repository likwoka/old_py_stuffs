#!/usr/bin/env python

"""
Simple multithread webserver.  Excellent performance, but
not very scalable (server may die due to unlimited RAM 
usage going upward, causing server to spiral to death). 
This is vulnerable to DOS attack.  
"""

from silverlib.quixote.server import threaded_server
from bookie import startup

startup.run(threaded_server.run, "quixote.conf", "bookie.conf")

