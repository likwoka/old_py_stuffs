#!/usr/bin/env python

'''
Usage: svnbox [OPTION]

List all subversion sandbox in the file system directories, as specified in
the configuration file.  The configuration file is looked up in the 
user home directory.  If it is not found and no configuration file is
specified on the command line, the program will ask the user to input a
list of directories to search for and generate a configuration file in the
user home directory.

Options:
    -c conffile, --conf conffile    use conffile as configuration file.
    -h, --help                      display this message
'''

import os, sys, getopt


USAGE = __doc_
__AUTHOR__ = "Alex Li <likwoka@yahoo.com>"
__VERSION__ = "0.2"
TMP_EXT = '.tmp'
SVN_DIR = '.svn'
FILENAME = '.svnbox.conf'


class UsageError(Exception):
    def __init__(self, msg=''):
        self.msg = msg


def parse_options(argv):
    '''Parse and return command line options and arguments.'''
    try:
        opts, args = getopt.getopt(argv, 'hc', ['help', 'conf'])
    except getopt.error, msg:
        raise UsageError(msg)
    
    conffile = None
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            raise UsageError(USAGE)
        if opt in ('-c', '--conf'):
            if len(args) != 1:
                raise UsageError('Missing configuration file parameter.')
            conffile = args[0]
    return conffile  # a string of conffile path


def get_config(conffile):
    '''Return the configuration parameters.
    1) if valid conffile is given in command line, use it;
    2) else look for user's home directory, if it is there, then use it;
    3) else ask the user questions, then create the file in the user 
    home directory.
    '''
    if conffile:
        if not os.path.isfile(conffile):
            raise UsageError('Configuration file <%s> is not found.' \
                             % conffile)
        config_vars = _read_conffile(conffile)
    else:
        import user
        c = os.path.join(user.home, FILENAME)
        if os.path.isfile(c):
            config_vars = _read_conffile(c)
        else:
            print 'No configuration file is found in your home directory.  ' \
                  'Svnbox will now attempt to create a configuration file ' \
                  'for you.  The file will be saved as %s in ' \
                  'your home directory.  Please answer the following ' \
                  'questions.' % FILENAME
            config_vars = _generate_conffile(c)
    return config_vars
    

def _read_conffile(conffile):
    '''Return configuration parameters from reading the config file.
    Config file is python code.
    '''
    config_vars = {}
    try:
        execfile(conffile, config_vars)
    except IOError:
        raise
    return config_vars


def _generate_conffile(conffile):
    '''Ask the user for a list of directories.'''
    dirs = raw_input('Please type in the directories (separate by ;):')
    dirlist = [path.strip() for path in dirs.split(';') 
               if len(path.strip()) > 0]
    f = file(conffile + TMP_EXT, 'w')
    f.write('dirlist = %s' % dirlist)
    f.close()
    os.rename(conffile + TMP_EXT, conffile)
    return {'dirlist': dirlist}


def is_svn_project(svnlist, dirname, files):
    if SVN_DIR in files:
        svnlist.append(dirname)
        del files[:]


def main(argv=None):
    if argv is None:
        argv = sys.argv    
    try:
        #0 is the script name, which we don't want
        conffile = parse_options(argv[1:])
        p = get_config(conffile)

        dirlist = p['dirlist']
        svnlist = []
        
        for path in dirlist:
            os.path.walk(path, is_svn_project, svnlist)

        print 'Subversion checkout at:' 
        for project in svnlist:
            print project
        print '%s Total' % len(svnlist)
            
    except UsageError, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 1


if __name__ == '__main__':
    sys.exit(main())
    
