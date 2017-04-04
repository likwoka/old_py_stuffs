2003 07 28

Purpose
=======
Control client machines (shutdown) from a central machine 
and keep track of their status (on/off).


Description
===========
The aktv project.  This project currently contains 3 parts.  

1) aktvendpoint.exe - a non commandline exe program for the karaoke client machine.
It sends a heartbeat to aktvcontrolpanel.exe, and accept XMLRPC commands from
aktvcontrolpanel.exe or aktvcontroller.exe.

2) aktvcontroller.exe - a commandline tool for sending command to aktvendpoint programs.

3) aktvcontrolpanel.exe - a GUI tool for controlling aktvendpoint programs.  It also
listens to heartbeat from aktvendpoint programs.


Requirement
===========
-python2.2
-pythonwin (for python2.2)
-wxpython2.4 (for python2.2)
-py2exe (For python2.2)


Build
=====
To create the exe:
1) cd to C:\sharedata\python\aktv

2) Run distutils setup for the program:

a) For endpoint.exe:
python setup_endpoint.py py2exe -w

b) For controlpanel.exe:
python setup_controlpanel.py py2exe -w --icon ico-file

c) For controller.exe
python setup_controller.py py2exe -c

