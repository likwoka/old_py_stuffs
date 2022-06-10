"""
Usage:
    clean_src.py -h
    clean_src.py /path/to/source

Clean the source code in Visual Studio.NET 2003 or 2005 solution by stripping 
the source control bindings, source control files, user settings files, and
the obj folders.

Options:
    -h, --help
"""

__VERSION__ = "2.0"

import os, sys, shutil, time, subprocess


USAGE = __doc__
TMP_EXT = ".tmp"
DEBUG = False


# Note: we want to keep *.csproj.webinfo
delete_files = ['vssver.scc', '.vspscc', 'mssccprj.scc', '.vsscc', '.vssscc',
                '.wdx', '.idx', '.suo', '_tmp.htm'] # '.csproj.user'

delete_dirs = ["obj", ".svn"] # "bin"


delete_lines_begin_with = {'.csproj' : ('Scc', '<Scc', '</Scc',),
                           '.vcproj' : ('Scc',),
                           '.dbp'    : ('Scc',),  # VS 2005 database project
                           '.vdproj' : ('"Scc',), # VS 2003 ? deployment project
                           '.sln'    : ('Scc',),} # WCF projects are stored in solution file!

delete_sections = {'.sln' : ('GlobalSection(SourceCodeControl)', 'EndGlobalSection'),
                   '.dsw' : ('begin source code control', 'end source code control'),}


class UsageError(Exception):
    def __init__(self, msg=""):
        self.msg = msg

        
def log(msg):
    """
    Display/log a message about the status and progress of this program.
    
    msg -- a string representing the message to display/log.
    """
    print(time.strftime("[%H:%M:%S]"), msg)


def set_files_to_writable(root_path):
    """
    Set files from readonly to writable.

    root_path -- all files under this path
                 will be set to writable.
    """
    log("Setting files from readonly to writable...")
    subprocess.call(['attrib', '-R', '/S', '/D'], cwd=root_path)


def walk_through(path):
    """
    Given a path, walk recursively to each folder and
    remove any files related to source control binding,
    and edit the project files to remove the source
    control binding lines.

    path -- a string of file system path
    """
    for root, folders, files in os.walk(path):

        for folder in folders:
            # Remove non essential folders.
            if folder in delete_dirs:
                shutil.rmtree(os.path.join(root, folder))
                del folder
    
        for name in files:
            # Remove unwanted files.
            for unwanted_name in delete_files:
                if name.endswith(unwanted_name):
                    os.remove(os.path.join(root, name))

                    ### DEBUG
                    if DEBUG: print("Removed unwanted file: %s" % os.path.join(root, name))
                    
            ext = os.path.splitext(name)[1]

            # If this is a project file, open it and
            # remove the Scc* attributes.  
            if ext in delete_lines_begin_with.keys():
                
                ### DEBUG
                if DEBUG: print("Start cleaning a project file: %s" % os.path.join(root, name))
                
                fullname = os.path.join(root, name)
                new_f = open(fullname + TMP_EXT, 'w')
                f = open(fullname, 'rU')

                unwanted_line_starts = delete_lines_begin_with[ext]
                               
                for line in f:
                    for u in unwanted_line_starts:
                        if line.strip().startswith(u):
                            break 
                    else:
                        new_f.write(line)  # Nothing match, we can write the line.
                        
                f.close()
                new_f.close()
                os.remove(fullname)
                os.rename(fullname + TMP_EXT, fullname)

            # If this is a solution file, open it and 
            # remove the SourceCodeControl sections. 
            if ext in delete_sections.keys():
                
                ### DEBUG
                if DEBUG: print("Start cleaning a solution file: %s" % os.path.join(root, name))
                
                fullname = os.path.join(root, name)
                new_f = open(fullname + TMP_EXT, 'w')
                f = open(fullname, 'rU')
                
                section_found = False
                section_start = delete_sections[ext][0]
                section_end = delete_sections[ext][1]
                
                for line in f:
                    # Look for start tag.
                    if line.strip().startswith(section_start):
                        section_found = True
                    
                    if section_found:
                        # Look for end tag.  We toggle the flag
                        # so lines after the end tag would get
                        # written out.
                        if line.strip().startswith(section_end):
                            section_found = False
                    else:
                        # Write out lines not belong to the 
                        # unwanted section.
                        new_f.write(line)

                f.close()
                new_f.close()
                os.remove(fullname)
                os.rename(fullname + TMP_EXT, fullname)


def main(path=None):
    try:
        if path is None:
            if len(sys.argv) != 2:
                raise UsageError(USAGE)

        path = sys.argv[1]

        if path == "-h" or path == "--help":
            raise UsageError(USAGE)
        
        log("Starting program.")
        abspath = os.path.abspath(path)

        if not os.path.exists(abspath):
            raise UsageError("<%s> does not exist!" % abspath)

        set_files_to_writable(abspath)
        walk_through(abspath)
        log("Done.")
        return 0
        
    except UsageError as err:
        print(err.msg, file=sys.stderr)
        return 1
    
                        
if __name__ == "__main__":
    sys.exit(main())

