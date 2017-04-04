#!/usr/bin/env python

'''
Usage: svn_change_repos [OPTION] root_directory old_pattern new_pattern

Starting from the root_directory, look for subversion directories.  
Once it is found, the entries file will be parsed, and the url
attribute of the <entry> tag will be matched.  If the "old" pattern
is found in the url attribute, it would be replaced by the "new"
pattern.

Options:
    -h, --help                      display this message

Examples:
    1) Change access protocol:
    svn_change_repos /home/userA http:// https://

    2) Change server:
    svn_change_repos /home/userA svn://192.168.1.1 svn+ssh://www.mysite.com
'''

import os, sys, getopt
from xml.dom import minidom


USAGE = __doc__
__AUTHOR__ = "Alex Li <likwoka@yahoo.com>"
__VERSION__ = "0.2"
SVN_DIR = '.svn'
TMP = '.TMP'


class UsageError(Exception):
    def __init__(self, msg=''):
        self.msg = msg


def parse_options(argv):
    '''Parse and return command line options and arguments.'''
    try:
        opts, args = getopt.getopt(argv, 'h', ['help',])
    except getopt.error, msg:
        raise UsageError(msg)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            raise UsageError(USAGE)
    
    if len(args) != 3:
        raise UsageError('Missing configuration file parameter.')
    
    return (args[0], args[1], args[2])


def is_svn_project(svn, dirname, files):
    '''
    Walker function of the os.walk() call.
    We walk all the directories, if it is called '.svn',
    we look for the 'entries' file and call swap_patterns()
    on it.  If we are in the '.svn' directory, there is
    no need to walk further down because no projects will be
    within '.svn' directories.
    
    svn - the dictionary containing the changed and unchanged lists,
          the oldpattern and new pattern.
    dirname - a string of the current directory name (no path attached)
    files - a string of the list of files within this directory 
            (no path attached)
    '''
    # We don't have to transverse inside this directory anymore
    if dirname == SVN_DIR:
        del files[:]
        return 
    
    if SVN_DIR in files:
        path = os.path.abspath(dirname)
        f = os.path.join(path, '.svn', 'entries')
        try:
            if swap_patterns(f, svn['oldpattern'], svn['newpattern']):
                # Add the project to the changed list
                # for reporting at the end.
                if is_top_level(path): 
                    svn['changed'].append(dirname)
            else:
                # Add the project to the unchanged list
                # for reporting at the end.
                if is_top_level(path):
                    svn['unchanged'].append(dirname)
        except IOError:
            print >> sys.stderr, 'IOError encountered processing file "%s"' % f


def is_top_level(path):
    '''
    Is this path (directory) the top level of a project?  If so
    then it is a project, otherwise it is just part of a project.
    
    path - a string of path.
    '''
    # Tackle the inner expression first...
    # Here we move to the parent directory's .svn directory;
    # then find out the absolute path expression for that;
    # then see if it exists or not.
    if os.path.exists(os.path.abspath(os.path.join(path, '..', '.svn'))):
        return False
    return True


def swap_patterns(filename, oldpattern, newpattern):
    '''
    Parse the file and swap the patterns.  If we swap
    anything, return True, else return False.

    filename - a string of the filename we are parsing
    oldpattern - a string of the old pattern
    newpattern - a string of the new pattern
    '''
    result = False
    dom = minidom.parse(filename)
    for entry in dom.getElementsByTagName('entry'):
        attr = entry.attributes.get('url')
        if attr:
            if attr.nodeValue.find(oldpattern) > -1:
                result = True
                attr.nodeValue = attr.nodeValue.replace(oldpattern, newpattern)

    # If we changed anything, write the changed file to a temp file 
    # to avoid race condition, then rename it to the original file.
    if result:
        # In Linux the 'entries' file is read-only, we need to change
        # that to allow write.
        if not os.access(filename, os.W_OK):
            # let's assume we have permission to change the permission
            # change it to rw- rw- rw-
            os.chmod(filename, 0666)
        
        tempname = filename + TMP
        dom.writexml(file(tempname, 'w'), newl='\n')
        
        # The following os.rename() will fail in Windows if the file "filename"
        # already exists.  Therefore we remove it first.  As noted, there may
        # never be a way for a x-platform atomic rename operation.
        if os.path.exists(filename):
            os.remove(filename)
        
        os.rename(tempname, filename)
        # The original permission is r-- r-- ---, 2004 07 11
        os.chmod(filename, 0440)
    return result
    

def main(argv=None):
    if argv is None:
        argv = sys.argv    
    try:
        #0 is the script name, which we don't want
        rootdir, oldpattern, newpattern = parse_options(argv[1:])
 
        svn = {'changed'    : [],
               'unchanged'  : [],
               'oldpattern' : oldpattern,
               'newpattern' : newpattern,}
               
        os.path.walk(rootdir, is_svn_project, svn)

        print >> sys.stdout, '\nChanged Subversion checkouts:' 
        for project in svn['changed']:
            print project
        print >> sys.stdout, '%s Total' % len(svn['changed'])
        
        print >> sys.stdout, '\nUnchanged Subversion checkouts:' 
        for project in svn['unchanged']:
            print project
        print >> sys.stdout, '%s Total\n' % len(svn['unchanged'])
             
    except UsageError, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 1


if __name__ == '__main__':
    sys.exit(main())

