#!/usr/bin/env python

"""
SCGI server (think of it as an app server)
Need a webserver as a frontend for web application.
See README.txt for Apache configuration file example.
"""

from quixote.server import scgi_server
from bookie import startup

startup.run(scgi_server.run, "quixote.conf", "bookie.conf")

