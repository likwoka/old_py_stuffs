from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from time import time, ctime, sleep
from threading import Thread, Event, Lock

import os, sys
from aktv import configurator


class Client(Thread):
    '''I give out heartbeat to a heartbeat listening server.'''

    def __init__(self, server_ip, beat_port, beat_interval, payload,
                 logger=None):
        '''Constructor.
        
        server_ip - string of the heartbeat server's ip address
        beat_port - int of the heartbeat server's listening port
        beat_interval - float of secs representing the interval between
                        each heartbeat
        payload - string of content of the udp heartbeat (<<<1024)
        logger - a file-like object for logging output and error.
                 Default is stdout.
        '''
        Thread.__init__(self)
        self._server_ip = server_ip
        self._beat_port = beat_port
        self._beat_interval = beat_interval
        self._payload = payload
        self._logger = logger or sys.stdout
        self._beat_event = Event()

    def run(self):
        '''Called by Thread.start() internally.'''
        while self._beat_event.isSet():
            print >> self._logger, 'Heart beat sent to IP %s:%s, %s' % \
                  (self._server_ip, self._beat_port, ctime(time()))
            hbsocket = socket(AF_INET, SOCK_DGRAM)
            hbsocket.sendto(self._payload, (self._server_ip, self._beat_port))
            sleep(self._beat_interval)

    def start(self):
        '''Starts the thread.'''
        self._beat_event.set()
        Thread.start(self)

    def stop(self):
        '''Stops and exit the thread.'''
        self._beat_event.clear()


class Recorder(Thread):
    '''I am a heartbeat listening server.  Once I
    receive a heartbeat, I will record it down using the
    update_func passed to me during initialization.
    '''
    
    def __init__(self, update_func, port, logger=None):
        '''The constructor.
        
        update_func(data, addr[0], port) - 
        where data, addr are returned from socket.socket(...).recvfrom(...)
        port - the heartbeat listening port
        logger - a file-like object for logging output and error.
                 Default is stdout.
        '''
        Thread.__init__(self)
        self._listen_event = Event()
        self._update = update_func
        self._logger = logger or sys.stdout
        self._recSocket = socket(AF_INET, SOCK_DGRAM)
        self._recSocket.bind((gethostbyname('localhost'), port))
        
    def run(self):
        '''Called by Thread.start() internally.'''
        while self._listen_event.isSet():
            #computer name is 32 byte at most... 1024 make it sort of general
            data, addr = self._recSocket.recvfrom(1024)
            print >> self._logger, 'Received packet from %s:%s %s' % \
                  (addr[0], addr[1], data)
            self._update(addr[0]) 
            
    def start(self):
        '''Starts the thread.'''
        self._listen_event.set()
        Thread.start(self)

    def stop(self):
        '''Stops and exits the thread.'''
        self._listen_event.clear()


class HeartBeatDict(dict):
    '''A dictionary of RoomRec.  Note that the update(...) method
    is synchronized.
    '''
    def __init__(self):
        self._lock = Lock()
    
    def update(self, ipaddr):
        '''Creates or updates a client entry.'''
        self._lock.acquire()
        self[ipaddr] = time()
        self._lock.release()