'''
aktvendpoint - runs a xmlrpc server for remote controlling (start/stop)
aktv.

Copyright (c) Alex Li 2003.  All rights reserved.

Use py2exe -w to compile it to a windows application (as oppose to
console application) for win32api.ExitWindowsEx() to work.
If python script, rename it from .py to .pyw

Parameters in aktvendpoint.ini:

# Essentials...
app_path = 'c:\\winnt\\notepad.exe'
app_startup_dir = None
port = 8080 			
start_app_when_initialize = True

# Controller
controller_ip = '127.0.0.1'
hb_port = 8080

# Access control
only_controller_ip_can_access = False
alt_access_list = []

# Logging error/output
log_file = 'aktvendpoint_log.txt'
append_to_file = False
'''

__VERSION__ = '0.2'
__AUTHOR__ = 'Alex Li <likwoka@yahoo.com>'


import sys, os, threading
import win32con, win32api, win32process
from aktv import xmlrpc, configurator, heartbeat


class app_process:
    '''I am the App Process.  I would be controlled by
    the client through XMLRPC.
    '''
    def __init__(self, app_name, app_startup_dir):
        self.app_name = app_name
        self.app_startup_dir = app_startup_dir
        self.started = False
        
    def start_app(self):
        if not self.started:
            app_name = self.app_name
            cmd_line = None
            process_attr = None
            thread_attr = None
            is_inherit_handles = 1
            creation_flags = 0
            new_environ = None
            current_dir = self.app_startup_dir
            startupinfo = win32process.STARTUPINFO()
            
            retval = win32process.CreateProcess(app_name, cmd_line,
                        process_attr, thread_attr, is_inherit_handles,
                        creation_flags, new_environ, current_dir,
                        startupinfo)
            self.hp = retval[0] #(hp, ht, pid, tid) = retval
            self.started = True
            return 'App started.'
        else:
            return 'App already started.'

    def stop_app(self):
        if self.started:
            win32process.TerminateProcess(self.hp, 0)
            self.started = False
            return 'App stopped.'
        else:
            return 'App already stopped.'


def cancel():
    global timer
    global is_timer_on
    if is_timer_on:
        timer.cancel()
        is_timer_on = False
    return 1

def shutdown_server_program(wait=0.1):
    return _do_action(wait, _shutdown_server_program)

def shutdown_machine(wait=0.1):
    return _do_action(wait, _shutdown_machine)

def _do_action(wait, action):
    wait = float(wait)
    if wait <= 0.0:
        wait = 0.1 # therefore we always return a value (ie, 1) in XMLRPC 

    global timer
    global is_timer_on

    #if not set already, we schedule it
    if not is_timer_on: 
        timer = threading.Timer(wait, action)
        timer.start()
        is_timer_on = True
    return 1    

def _shutdown_server_program():
    '''I allow the XMLRPCServer to be killed remotely.'''
    global a, heart_thread, out, server
    a.stop_app() #stop the app before killing the server
    heart_thread.stop()
    out.close()
    os._exit(0)
    server.stop()
    return 1 #if just return, you will get a 500 internal server error

def _shutdown_machine():
    #ExitWindowsEx() is asynchronous... we can call it
    #and then continue to shutdown the server program...
    #Win95/98 only ... need win32security.AdjustTokenPrivileges() for win2k
    win32api.ExitWindowsEx(1)
    return _shutdown_server_program()

def restart_machine():
    win32api.ExitWindowsEx(2) #Win95/98 only
    return _shutdown_server_program()

def get_machine_name():
    name = win32api.GetComputerName()
    return name


if __name__ == '__main__':
    c = configurator.get_param(os.path.join(sys.path[0], 'aktvendpoint.ini'))

    # Starts logging options
    if c['append_to_file']:
        mode = 'a'
    else: mode = 'w'
    out = file(os.path.join(sys.path[0], c['log_file']), mode)
    #sys.stderr = sys.stdout = out

    # Starts app
    a = app_process(c['app_path'], c['app_startup_dir'])
    if c['start_app_when_initialize']:
        a.start_app()

    # Starts sending heart beat to the controller in another thread
    payload = get_machine_name()
    heart_thread = heartbeat.Client(c['controller_ip'],
                                    c['hb_port'],
                                    c['hb_interval'],
                                    payload, out)
    heart_thread.start()

    # Prepare timer thread variables
    is_timer_on = False
    timer = None
    
    # Starts XMLRPCServer for listening to command from the controller
    # on the main thread
    server = xmlrpc.XMLRPCServer(c['controller_ip'],
                                 c['only_controller_ip_can_access'],
                                 c['alt_access_list'], '', c['port'])
    server.register_instance(a)
    server.register_function(shutdown_server_program)
    server.register_function(shutdown_machine)
    server.register_function(restart_machine)
    server.register_function(get_machine_name)
    server.register_function(cancel)
    server.serve_forever()

    

