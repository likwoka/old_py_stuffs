"""
%prog /path/to/sln_file [Options]

Description:
    Change the output directories of C# library projects to 
    binEDC.  Only non-web C# project will be changed.  The 
    path to binEDC will be relative. 

    Normally you would use this on tierWebServices.sln only.
 
Example:
    %prog /path/to/sln_file
    %prog /path/to/sln_file -o /path/to/alt/binEDC -b Debug

Compatibility:
    VS.NET 2003
     
Requirement:
    Python 2.5+, ablib.py
"""

USAGE = __doc__
VERSION = "0.3"


import os, sys, optparse, traceback, shutil, tempfile
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

from ablib import SolutionFile, set_file_to_writable, get_relative_path



def has_build(proj_path, build_tags):
    try:
        root = ElementTree.parse(proj_path)
        proj_type = root.find("CSHARP").get("ProjectType")
        
        if proj_type == "Local":
            configs = root.findall("CSHARP/Build/Settings/Config")
            for config in configs:
                if config.get("Name") in build_tags:
                    return True
        return False
    except Exception:
        print >> sys.stderr, "Error parsing %s, see traceback below:" % proj_path
        traceback.print_exc()
        return False



def change_outputpath(proj_name, proj_path, build_tags, binedc_path, is_dry_run):
    f = open(proj_path, 'rU')
    in_lines = f.readlines()
    f.close()
    
    temp_fd, temp_path = tempfile.mkstemp()
    new_f = os.fdopen(temp_fd, "w+b")

    build_found = False
    build_start = "Name" 
    
    section_found = False
    section_start = "<Config"

    outputpath_start = "OutputPath"
    
    for in_line in in_lines:
        line = in_line.strip()
        
        # Look for start tag.
        if line.startswith(section_start):
            section_found = True
            out_line = in_line

        elif section_found and line.startswith(build_start):
            
            current_build = line.split('"')[1]
            if current_build in build_tags:
                build_found = True
            out_line = in_line
        
        elif build_found and section_found and line.startswith(outputpath_start):
            section_found = False
            build_found = False 
            
            current_path = line.split('"')[1]
            if current_path != binedc_path:
                out_line = in_line.replace(current_path, binedc_path)
                print >> sys.stdout, "%s %s changed from %s to %s" % (
                        proj_name, current_build, current_path, binedc_path)
            else:
                out_line = in_line
        else:
            out_line = in_line
        new_f.write(out_line)

    new_f.close()
    if not is_dry_run:
        shutil.copy(temp_path, proj_path)
    os.remove(temp_path)


def main():
    try:
        parser = optparse.OptionParser(USAGE)
        parser.add_option("-b", "--build-tags",
                action="store", dest="build_tags", default="Release,Debug",
                help="the builds we are interested in; Default is Release,Debug")
        parser.add_option("-o", "--output-path",
                action="store", dest="binedc_path", default=None,
                help="path to the output folder; Default is binEDC in the solution file's folder.")
        parser.add_option("-n", "--dry-run",
                action="store_true", dest="is_dry_run", default=False,
                help="Don't actually do any changes, just print out the intended result.")
        opts, args = parser.parse_args()
    
        num_of_args = len(args)
        if num_of_args != 1:
            print >> sys.stderr, "Invalid number of input arguments!"
            return 1  
        
        sln_path = os.path.abspath(args[0])
        if not os.path.isfile(sln_path):
            print >> sys.stderr, "%s is not a file!" % sln_path
            return 1
        build_tags = opts.build_tags.split(",")
        
        if opts.binedc_path:
            binedc_path = os.path.abspath(opts.binedc_path)
        else:
            binedc_path = os.path.join(os.path.dirname(sln_path), "binEDC")

        for p in SolutionFile(sln_path).get_projects():
            proj_name  = p.proj_name
            proj_path  = p.proj_path
            
            if has_build(proj_path, build_tags):
                if not opts.is_dry_run:
                    set_file_to_writable(proj_path)
                
                correct = get_relative_path(proj_path, binedc_path)
                
                change_outputpath(proj_name, proj_path,
                        build_tags, correct, opts.is_dry_run)
            else:
                print >> sys.stderr, "Builds %s don't exist in %s" % (
                        ", ".join(build_tags), proj_path)
        
        return 0

    except Exception:
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
