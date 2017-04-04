#!/usr/bin/env python

"""
Usage: 
    makepydoc.py [Options]
    makepydoc.py -o /path/to/output -n os
    makepydoc.py --output=/path/to/output --namespace=os
   
Make pydoc documents for a namespace, which can be a module, a package and
its subpackages.
    
Options:
    -o, --output        Output directory (Default to current directory)
    -n, --namespace     The namespace
    -h, --help
"""

USAGE = __doc__
__VERSION__ = "0.2.1"
__AUTHOR__ = "Alex Li <likwoka@yahoo.com>"

# %s is the module name.
CMD = "/usr/bin/pydoc -w %s"
EXTS = [".py", ".pyc", ".pyo"]


import os, sys, getopt


class UsageError(Exception):
    def __init__(self, msg=""):
        self.msg = msg


def parse_options(argv):
    """
    Parse and return command line options and arguments.

    argv -- a list of argumetns/options in the input.
    """
    try:
        opts, args = getopt.getopt(argv, "ho:n:", 
                                   ["help", "output=", "namespace="])
    except getopt.error, msg:
        raise UsageError(msg)

    options = {"output": os.getcwd()}
  
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            raise UsageError(USAGE)
        if opt in ("-o", "--output"):
            options["output"] = arg
        if opt in ("-n", "--namespace"):
            options["namespace"] = arg

    if options.get("namespace", None) is None:
        raise UsageError("Please give a namespace argument.")
    
    return options


def is_package(dir):
    """
    Is this directory a package/subpackage?

    dir -- a string of the path to the package's directory.
    """
    for ext in EXTS:
        if os.path.exists(os.path.join(dir, "__init__" + ext)):
            return True
    return False


def call_pydoc(the_namespace):
    """
    Open a pipe to a subprocess calling pydoc.

    the_namespace -- a string of the namespace argument we call pydoc with.
    """
    dummy, out, err = os.popen3(CMD % the_namespace, "r")
    err_buffer = err.readlines()
    
    # Is there any error?
    if len(err_buffer) == 0:
        print >> sys.stdout, "%s ... OK" % the_namespace
    else:
        print >> sys.stderr, "%s ... ERROR %s" % (
            the_namespace, "/".join(err_buffer))
    
    dummy.close()
    out.close()
    err.close()


def walk(dir, namespace):
    """
    Walk recursively through a package and its subpackages.

    dir -- a string of the path to the package's directory.
    namespace -- the current namespace representing this package.
    """
    last_module = ""
    
    for f in os.listdir(dir):
        
        the_path = os.path.join(dir, f)
        
        if os.path.isfile(the_path):
            # Handle all modules here.
            module = os.path.splitext(f)[0]
            
            # This check is for cases where 
            # there are multiple files for the 
            # same module in the same directory,
            # ex: a.py, a.pyc, a.pyo
            if module != last_module:
                call_pydoc("%s.%s" % (namespace, module))
                last_module = module

        elif os.path.isdir(the_path):
            # Handle all subpackages here.
            if is_package(the_path):
                subpackage = f
                call_pydoc("%s.%s" % (namespace, subpackage))
                walk(the_path, "%s.%s" %(namespace, subpackage))


def main(argv=None):
    if argv is None:
        # No argument is passed in through the function,
        # let's get the command line input, minus the
        # script name itself.
        argv = sys.argv[1:]
    try:
        options = parse_options(argv)
        
        # Change the current working directory to the
        # output directory.
        os.chdir(options["output"])
        
        # We import the namespace to determine its location.
        namespace = __import__(options["namespace"])
        dir, file = os.path.split(namespace.__file__)
        
        if os.path.splitext(file)[0] == "__init__":
            # This is a package, we need to get all 
            # its subpackage and modules.
            call_pydoc(options["namespace"])
            walk(dir, options["namespace"])
        else:
            # This is just a single module, which means
            # only a single file.
            call_pydoc(options["namespace"]) 
        
    except UsageError, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "For help use --help"
        return 1
    

if __name__ == "__main__":
    sys.exit(main())

