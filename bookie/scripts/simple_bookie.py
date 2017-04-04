#!/usr/bin/env python

"""
Simple single thread demo webserver.
"""

from quixote.server import simple_server
from bookie import startup

startup.run(simple_server.run, "quixote.conf", "bookie.conf")
