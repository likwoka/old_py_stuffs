"""%prog /path/to/sln_file [Options]

Description:
    A utility to find out the references of projects in a solution file.

    By default without any option, it will list out the current
    non-microsoft binary references, and if there is a equivalent 
    project references in the solution.

    To change the non-Microsoft binary references to project 
    references, if possible, use the -p option.

    To change the non-Microsoft binary references to binary
    references in another location, use the -b option, and 
    state the original root and new root separated with a 
    comma.  In addition, by combining the -v option, it 
    will verify if the new binary reference path exists 
    before changing.

Example:
    %prog /path/to/sln_file
    %prog /path/to/sln_file -p
    %prog /path/to/sln_file -p -n 
    %prog /path/to/sln_file -b /path/to/orig_root,/path/to/new_root -n
    %prog /path/to/sln_file -b /path/to/orig_root,/path/to/new_root -v 
    %prog /path/to/sln_file -b /path/to/orig_root,/path/to/new_root -v -n

Compatibility:
    VS.NET 2003     

Requirement:
    Python 2.5+, ablib.py""" 


USAGE   = __doc__
VERSION = "0.1"

MS_BIN1 = "Microsoft.NET\\Framework"
MS_BIN2 = "Microsoft.NET\Primary Interop Assemblies"


import os, sys, optparse, traceback, shutil, tempfile
from os.path import join, normpath, dirname, basename, splitext
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

from ablib import SolutionFile, set_file_to_writable



def get_projects_with_bin_refs(projects):
    """Return a list of projects that have non-MS binary references in them.

    projects -- a list of all projects in a solution file."""
    result = []
    for p in projects:
        try:
            root = ElementTree.parse(p.proj_path)
            refs = root.findall("CSHARP/Build/References/Reference")
            nonms_bin_refs = []
            for ref in refs:
                assembly_name = ref.get("AssemblyName")
                hint_path = ref.get("HintPath")
                if (hint_path != None 
                    and MS_BIN1 not in hint_path
                    and MS_BIN2 not in hint_path):
                        nonms_bin_refs.append(
                            (assembly_name,
                             hint_path,
                             normpath(join(dirname(p.proj_path), hint_path)))
                        )
                    
            if len(nonms_bin_refs) > 0:
                p.nonms_bin_refs = nonms_bin_refs
                result.append(p)
        except Exception:
            print >> sys.stderr, "Error parsing %s, see traceback below:" % p.proj_path
            traceback.print_exc()
    return result


def get_asmname_mapping(projects):
    """Return a dict of assembly_name : proj_guid for all projects
    in a solution file.

    projects -- a list of all projects in a solution file."""
    result = {}
    for p in projects:
        try:
            root = ElementTree.parse(p.proj_path)
            settings = root.find("CSHARP/Build/Settings")
            assembly_name = settings.get("AssemblyName")
            result[assembly_name] = p.proj_guid
        except Exception:
            print >> sys.stderr, "Error parsing %s, see traceback below:" % p.proj_path
            traceback.print_exc()
    return result


def change_to_proj_refs(projects, package_guid, asmname_mapping, is_dry_run):
    """Change non-MS binary references in projects to project references,
    if they are contained in the same solution file.

    projects -- the list of projects with non-MS binary references.
    package_guid -- a string of package_guid, which is the GUID of 
                    a solution file.
    asmname_mapping -- a dictionary of assembly_name : project_guid 
                 for all projects in the solution file.
    is_dry_run -- a bool indicates whether to really do it or not."""
    for p in projects:
        # a dict of assembly_name : proj_guid
        new_proj_refs = {}
        for (assembly_name, hint, full) in p.nonms_bin_refs:
            if assembly_name in asmname_mapping:
                new_proj_refs[assembly_name] = p.proj_guid

        # Now we change the project file with those new hint paths.
        if not is_dry_run:
            set_file_to_writable(p.proj_path)
            f = open(p.proj_path, 'rU')
            in_lines = f.readlines()
            f.close()
            
            temp_fd, temp_path = tempfile.mkstemp()
            new_f = os.fdopen(temp_fd, "w+b")

            ref_node = False
            replace = False

            for in_line in in_lines:
                stripped_line = in_line.strip()
                if stripped_line.startswith("<Reference"):
                    ref_node = True
                    out_line = in_line
                elif stripped_line.startswith("/>") and ref_node == True:
                    ref_node = False
                    replace  = False
                    out_line = in_line
                elif stripped_line.startswith("AssemblyName") and ref_node == True:
                    coms = in_line.split('"')
                    if coms[1] in asmname_mapping:
                        replace = True
                        proj_guid = asmname_mapping[coms[1]]
                        out_line1 = '"'.join([coms[0].replace("AssemblyName", "Project"), proj_guid, ""])
                        out_line2 = '"'.join([coms[0].replace("AssemblyName", "Package"), package_guid, ""])
                        out_line = "\n".join([out_line1, out_line2])
                    else:
                        out_line = in_line
                elif stripped_line.startswith("HintPath") and ref_node == True and replace == True:
                    out_line = ""
                else:
                    out_line = in_line
                new_f.write(out_line)

            new_f.close()
            shutil.copy(temp_path, proj_path)
            os.remove(temp_path)
        
        # Feedback to user.
        for (k, v) in new_proj_refs.items():
            print >> sys.stdout, "%s: Changed binary reference to project reference for %s." % (
                    p.proj_name, k)


def change_to_bin_refs(projects, orig_root, new_root, is_dry_run, should_verify):
    """Change the projects with non-MS binary references from the
    original root location to the new root location.  

    projects -- the list of projects with non-MS binary references.
    orig_root -- a string of the original root of the binary references.
    new_root -- a string of the new root for the binary references.
    is_dry_run -- a bool indicates whether to really do it or not.
    should_verify -- a bool indicates if the new binary references should 
                     be tested out first before really change."""
    for p in projects:
        # a dict of "old_hint" : (new_hint, new_full_path) for all
        # non-MS binary references.
        new_bin_refs = {}

        # Create all new hint paths first.
        for (_, hint, full) in p.nonms_bin_refs:
            if not full.startswith(orig_root):
                print >> sys.stderr, "The binary reference path %s for %s does not belong to %s" % (
                        full, p.proj_name, orig_root)
                continue

            new_full = full.replace(orig_root, new_root)
            new_hint = join(get_relative_path(p.proj_path, new_full), basename(hint))
            
            # If the new hint paths is not valid, then leave
            # it out of the new_bin_refs dictionary.
            if should_verify:
                if not os.path.exists(new_full):
                    print >> sys.stderr, "The new binary reference path %s for %s does not exist!" % (
                            new_full, p.proj_name)
                else:
                    new_bin_refs[hint] = (new_hint, new_full)
            else:
                new_bin_refs[hint] = (new_hint, new_full)

        # Now we change the project file with those new hint paths.
        if not is_dry_run:
            set_file_to_writable(p.proj_path)
            f = open(p.proj_path, 'rU')
            in_lines = f.readlines()
            f.close()
            
            temp_fd, temp_path = tempfile.mkstemp()
            new_f = os.fdopen(temp_fd, "w+b")

            for in_line in in_lines:
                if in_line.strip().startswith("HintPath"):
                    begin, old_hint, end = in_line.split('"')
                    out_line = '"'.join([begin, new_bin_refs[old_hint][0], end])
                else:
                    out_line = in_line
                new_f.write(out_line)

            new_f.close()
            shutil.copy(temp_path, proj_path)
            os.remove(temp_path)
        
        # Feedback to user.
        for (k, v) in new_bin_refs.items():
            print >> sys.stdout, "Changed binary reference for %s from %s to %s." % (
                    p.proj_name, k, v[0])


def pretty_print(projects, asmname_mapping):
    """Print the projects and their non-MS binary references.

    projects -- the list of project.
    asmname_mapping -- a dictionary of assembly_name : project_guid 
                 for all projects in the solution file."""
    for i, proj in enumerate(projects):
        print >> sys.stdout, "%-3d %s" % (i+1, proj.proj_name)
        
        for j, (_, hint, full) in enumerate(proj.nonms_bin_refs):
            have_proj = "YES" if splitext(basename(hint))[0] in asmname_mapping else "NO" 
            
            print >> sys.stdout, "\t%-3d %s" % (j+1, hint)
            print >> sys.stdout, "\t\tFull Path: %s" % full
            print >> sys.stdout, "\t\tProject Reference: %s" % have_proj
            #print >> sys.stdout, "\t\tsplitext(basename(hint))[0]: %s" % splitext(basename(hint))[0]
            print >> sys.stdout, ""


def main():
    try:
        parser = optparse.OptionParser(USAGE)

        parser.add_option("-p", "--project-reference",
                action="store_true", dest="to_project", default=False,
                help="Convert possible binary references to project references according to the solution file.")

        parser.add_option("-b", "--binary-reference",
                action="store", dest="orig_n_new_roots", default=None,
                help="Convert possible binary references from one location to another.")

        parser.add_option("-v", "--verify-existence",
                action="store_true", dest="should_verify", default=False,
                help="Verify if the new binary reference paths exist before changing.")

        parser.add_option("-n", "--dry-run",
                action="store_true", dest="is_dry_run", default=False,
                help="Don't actually do any changes, just print out the intended result.")
        
        opts, args = parser.parse_args()
        num_of_args = len(args)
        if num_of_args < 1:
            print >> sys.stderr, "Invalid number of input arguments!"
            return 1  

        sln_path = os.path.abspath(args[0])
        if not os.path.isfile(sln_path):
            print >> sys.stderr, "%s is not a file!" % sln_path
            return 1

        sln = SolutionFile(sln_path)
        all_projects = sln.get_projects()
        bin_projects = get_projects_with_bin_refs(all_projects)

        # -p option. Can have -n at the same time.
        if opts.to_project:
            package_guid = sln.get_package_guid()
            asmname_mapping = get_asmname_mapping(all_projects)
            change_to_proj_refs(bin_projects, package_guid,
                    asmname_mapping, opts.is_dry_run)
        
        # -b option. Can have -n or -v at the same time.
        elif opts.orig_n_new_roots:
            orig_root, new_root = orig_n_new_roots.split(",", 2)
            orig_root = abspath(orig_root)
            new_root  = abspath(new_root)

            change_to_bin_refs(bin_projects, orig_root, new_root,
                    opts.is_dry_run, opts.should_verify)
        
        # No option.  Just list the result.
        else:
            asmname_mapping = get_asmname_mapping(all_projects)
            pretty_print(bin_projects, asmname_mapping)
            return 0 

    except Exception:
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
