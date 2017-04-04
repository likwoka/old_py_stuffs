"""
%prog [options]

Examples:
    %prog
    %prog -c /path/to/configfile.conf
    %prog -g
    %prog -h
    %prog -n

Backup a folder to a backup location.  Require python 2.4+ and 
rsync (or rsync.py 2.0).  Alex Li (likwoka@gmail.com), 2006.
"""

# TODO: Add Archive mode support (refactor code first)

import subprocess, os, optparse, time, sys, platform


USAGE = __doc__

VERSION = '0.5'
TMP_EXT = ".tmp"
CONFIG_PATH = "backup.conf"
REPORT_PATH = "README.%s.txt"


CONFIG_CONTENT = r'''# Configuration file for backup.py version %s

# The tuple is ("sync this folder", "to this location")
sync_set = [
    (r'/important/folder', r'/some/backup/drive/mybackup'),
    (r'/another/important/folder', r'/some/backup/drive/mybackup'),
    (r'/important/file', r'/some/backup/drive/mybackup'),
]

# Exclude these folders or files
sync_exclude = [
    r"important/folder/garbage",
    r"important/folder/outdated_file.txt",
    ]

# Where to put the log
log_dir = r"/some/directory"

# Path to the rsync executable.
rsync = r"/usr/local/bin" 
''' 


REPORT_CONTENT = r'''
backup.py (version %s) last run at %s.
Synced up these folders (from, to) on machine %s:
%s
Skipping these folders:
%s
'''


class UsageError(Exception):
    def __init__(self, msg=""):
        self.msg = msg


def log(msg):
    """
    Display/log a message about the status and progress of this program.
    
    msg -- a string representing the message to display/log.
    """
    print time.strftime("[%H:%M:%S]"), msg


def generate_config_file(path):
    """
    Generate a sample config file for this program..

    path -- the name of the config file.
    """
    f = open(path + TMP_EXT, 'w')
    f.write(CONFIG_CONTENT % VERSION)
    f.close()
    os.rename(path + TMP_EXT, path)


def read_config_file(path):
    """
    Given the path to the config file, return a 
    dict instance of settings.  The settings
    are processed (and checked) in this function.
    
    path -- a string of path to the config file.
    """
    settings = {}
    execfile(path, settings)
    
    # We will be doing a bunch of path gymnastic below
    # to satisfy rsync.
    
    sync_set = []
    for (from_dir, to_dir) in settings["sync_set"]:
        
        # Processing the from_dir param.  At the end of it, the path
        # would be:
        # d:\home\alex  --> NO CHANGE
        # /home/alex    --> NO CHANGE
        # /home/alex/   --> /home/alex
        # d:\home\alex\ --> d:\home\alex 
        from_dir = os.path.abspath(from_dir)
        
        if not os.path.exists(from_dir):
            raise UsageError("The source %s does not exists!" % from_dir)

        if os.path.isdir(from_dir) and from_dir.endswith(os.path.sep):
            from_dir = from_dir[:-1]

        # Processing to_dir param.  At the end of it, the path would be:
        # g:\backup\laptop (with d:\home\alex)  --> g:\backup\laptop\d\home
        # /backup/laptop (with /home/alex)      --> /backup/laptop/home 
        to_dir = os.path.abspath(to_dir)
        
        # Concat the root of the destination and the backup folder together,
        # this will be the real destination...
        
        # Chop the immediate from directory away...
        from_dir_root = os.path.split(from_dir)[0]
        
        # To take care of linux and mac, or else windows.
        if from_dir_root[0] in ("\\", "/"):
            destination = from_dir_root[1:]
        else:
            destination = from_dir_root.replace(":", "")
            
        to_dir = os.path.join(to_dir, destination)
        
        if os.path.exists(to_dir):
            if not os.path.isdir(to_dir):
                raise UsageError("The backup location %s does not exists!" % to_dir)
        else:
            os.makedirs(to_dir)

        sync_set.append( (from_dir, to_dir) )

    settings["sync_set"] = sync_set
        
    # Processing sync_exclude list.  At the end of it, the paths in
    # the sync_exclude list would be:
    # /home/alex/hello      --> alex/hello
    # d:\home\alex\hello    --> home\alex\hello
    # bin                   --> NO CHANGE
    # *.swp                 --> NO CHANGE
    sync_exclude = []
    prefix = os.path.split(from_dir)[0]
    for e in settings["sync_exclude"]:
        if e.startswith(prefix):
            e = e[len(prefix):]
                              
        # After taking out the from_dir, the sync_exclude path
        # may be starting with a / or \, which could confuse
        # rsync, so we remove it.
        if e[0] in ("\\", "/"):
            path = e[1:]
        else:
            path = e
        
        sync_exclude.append('--exclude="%s"' % path)
    settings["sync_exclude"] = sync_exclude
    
    log_dir = os.path.abspath(settings["log_dir"])
    if os.path.exists(log_dir):
        if not os.path.isdir(log_dir):
            raise UsageError("The log folder %s does not exists!" % log_dir)
    else:
        os.makedirs(log_dir)
    settings["log_dir"] = log_dir
    
    return settings


def sync(settings):
    """
    Synchronize the folders (from_dir -> to_dir).  It is
    a 1-way sync.

    settings -- a dict containing all the configuration
                settings.
    """
    rsync = settings["rsync"]
    cwd   = os.getcwd()
    
    call = [rsync, '-r', '-t', '--delete']
    if settings.get("dry_run", False): call += ['-n']
    call += settings['sync_exclude']
    
    for (from_dir, to_dir) in settings["sync_set"]:

        if from_dir.find(" ") > -1:
            from_dir = '"%s"' % from_dir

        if to_dir.find(" ") > -1:
            to_dir = '"%s"' % to_dir

        call += [from_dir, to_dir]
        
        print 
        print " ".join(call)
        print
        
        # XXX Has to pass in a string, rather than a list!
        # A subprocess bug?
        retcode = subprocess.call(" ".join(call), shell=True)


def write_summary(settings):
    """
    Write the backup summary to a file.

    path -- the name of the summary file.
    """
    if settings.get("dry_run", False):
        return

    timestamp = time.ctime()
    machine = str(platform.uname())
    exclude = "\n".join(settings["sync_exclude"])
    sync_list = "\n".join(["%s, %s" % (f, t) for (f, t) in settings["sync_set"]])
    
    path = os.path.join(settings["log_dir"], REPORT_PATH % time.strftime("%Y%m%d"))

    f = open(path + TMP_EXT, 'w')
    f.write(REPORT_CONTENT % (VERSION, timestamp, machine, sync_list, exclude))
    f.close()

    if os.path.exists(path):
        os.remove(path)
    os.rename(path + TMP_EXT, path)

    
def main():
    try:
        parser = optparse.OptionParser(USAGE)
        parser.add_option('-g', '--generate', action='store_true',
                help="generate a sample configuration file " +
                "in the current working directory")
        parser.add_option('-v', '--version', action='store_true',
                help="display the version info")
        parser.add_option('-n', '--dry-run', action='store_true',
                help="Show what would happen; don't actually run it")
        parser.add_option('-c', '--config',
                help="specify the configuation file location")

        (options, args) = parser.parse_args()
        
        if options.version:
            print VERSION
            return 0

        elif options.generate:
            path = os.path.join(os.getcwd(), CONFIG_PATH)
            generate_config_file(path)
            print "Sample configuration file created at", path
            return 0
        
        else:
            log("Starting backup...")
            if options.config:
                path = os.path.abspath(options.config)
                if not os.path.exists(path):
                    raise parser.error("Configuration file %s does not exist!" % path)
            else:
                path = os.path.join(os.getcwd(), CONFIG_PATH)
            
            log("Parsing configuration file...")
            settings = read_config_file(path)

            if options.dry_run:
                settings["dry_run"] = True;
            
            log("Syncing files to backup location...")
            sync(settings)
            
            log("Writing summary report...")
            write_summary(settings)
            
            log("Done.")
            return 0
            
    except UsageError, err:
        print >> sys.stderr, err.msg
        return 1


if __name__ == '__main__':
    sys.exit(main())

