'''
sumsales.py [OPTION] [DIRECTORY]

OPTION:
-h, --help      Print this help message.

This program produces a sales summary report for a month in Excel
file format.  If the directory path is not given as a command line
argument, then the GUI mode will be invoked.
'''


# Command Line Mode, non-interactive mode (GUI)
import getopt, os, sys
from sumsales import core


class UsageError(Exception):
    def __init__(self, msg=''):
        self.msg = msg


def commandline(argv):
    '''The non-interactive mode.'''
    try:
        try:
            opts, args = getopt.getopt(argv, 'h', ['help',])
        except getopt.error, msg:
            raise UsageError(msg)
            
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                raise UsageError(__doc__)

        if len(args) != 1:
            raise UsageError('You did not tell me which folder.')
        if not os.path.isdir(args[0]):
            raise DirectoryNotFoundError(args[0])
       
        path = args[0]
        
        core.sum(path)
        
    except UsageError, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 1


if __name__ == "__main__":
    argv = sys.argv[1:] # 0 is the script name itself    
    sys.exit(commandline(argv))
