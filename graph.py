'''
Generate a assemblies dependency graph from available source code.
Note that this shows the assembly dependencies at compile time only.  
However, the runtime dependencies would be the same if no 
System.Reflection calls are used! 

Usage:
    graph.py path_to_solution.sln

Example:
    graph.py /path/to/solution.sln 
    graph.py /path/to/solution.sln -d
    graph.py -h


Options:
    -h, --help
    -d, --debug

Requirement: 
    Python 2.4+, Graphviz, pyparsing, and pydot
''' 


USAGE = __doc__
VERSION = '0.6 (20120712)'
AUTHOR = 'Alex Li (likwoka@gmail.com)'


import sys, os, random
from xml.dom import minidom
import pydot

# TODO:
# Do we still want to keep assembly version?
# If background color is dark, use white foreground color (and vice versa).
# Tweak the layout so that it is not so wide
# Try client-side map and URL within node!
# Tool tips to give more info?


IGNORE_LIST = [
    'System', 
    'System.Configuration',
    'System.Core',
    'System.Data',
    'System.Data.DataSetExtensions',
    'System.Deployment',
    'System.Drawing',
    'System.Runtime.Caching',
    'System.Runtime.Serialization',
    'System.Web',
    'System.Xml',
    'System.Xml.Linq',
    'Microsoft.CSharp',]


class UsageError(Exception):
    def __init__(self, msg=""):
        self.msg = msg


UNKNOWN = "unknown"

class Project:
    '''In graph theory terms, this is the node.  
    The depends_on property contains the arcs.
    '''
    def __init__(self, name):
        '''Constructor.
        
        name -- a str of the project name
        '''
        self.name = name
        self.path = UNKNOWN
        self.proj_guid = UNKNOWN
        self.assembly_name = UNKNOWN
        self.assembly_version = UNKNOWN
        self.depends_on = []


class SolutionFileParser:
    '''Parse the .sln file to extract the list of projects/assemblies to 
    be included in the graph.
    '''
    def __init__(self, path):
        '''Constructor.
        
        path -- a str of the solution's path
        '''
        self.path = path

    def is_project_line(self, line):
        '''Return true if this line in the solution file represents a project,
        return false otherwise.
        
        line -- a str of the line
        '''
        if line.startswith('Project("'):
            return True
        return False

    def parse_file(self):
        '''Parse the solution file, return a dictionary of name : project instance
        (str : obj).
        '''
        WEB_PATH = "http://localhost/"
        START = len(WEB_PATH)
        root = os.path.dirname(self.path)
        projects = {}

        for line in open(self.path, 'r'):
            if not self.is_project_line(line):
                continue

            # Line is Project("PACKAGE_GUID") = "NAME", "PATH", "PROJ_GUID"     
            name, path, proj_guid = (i.strip() for i in line.split(","))
            
            name = name.split("=")[1].strip().replace('"', '')
            if name in IGNORE_LIST:
                continue
   
            proj_guid = proj_guid.replace('"', '')

            path = path.replace('"', '')
            
            if not path.endswith(".csproj"): # to ignore .vdproj or just folder
                continue
            
            if path.startswith(WEB_PATH):
                # Is a webproject.
                path = os.path.join(root, path[START:])
            elif path.find(":") == -1:
                # Is a relative path.
                path = os.path.join(root, path)
            else:
                # No need to do special handling on the path. 
                pass 
 
            p = Project(name)
            p.proj_guid = proj_guid
            p.path = path

            projects[name] = p
        return projects

        
def ParserFactory(path):
    '''Return a ProjParser class depending on the verson of the solution file. 
    Insight: The VS solution file formats are pretty much the same across
    different versions, but the project file formats have changed a lot.

    path -- a str of path to the solution file.
    '''
    f = open(path, 'r')
    line = f.readline().strip()
    while not line.startswith("Microsoft Visual Studio Solution File"):
        line = f.readline().strip()
    f.close()

    if line.endswith("8.00"):
        return VS2003ProjParser
    elif line.endswith("9.00"):
        return VS2010ProjParser     # compatible
    elif line.endswith("10.00"):
        raise VS2010ProjParser      # compatible
    elif line.endswith("11.00"):
        return VS2010ProjParser
    else:
        raise NotImplementedError("ProjParser not implemented for this version of VS.")

        
class ProjParserBase:
    '''A base class for a project file parser.
    '''
    def __init__(self, path, projects):
        '''Constructor.
        
        path -- a str of the project file's path
        projects -- a dict of name-projects.  This is the "Master List"
                    of projects found in the solution file.
        '''
        self.path = path
        self.projects = projects
        
    def parse_file(self, project):
        '''Parse the project file of this particular project instance.
        We do this to find out the dependency of this project on others.
        Return a tuple of the updated project instance, and extra project 
        dependencies (in a dictionary).
        
        project -- an instance of the project   
        '''    
        raise NotImplementedError("This is a base class.")
        
       
class VS2003ProjParser(ProjParserBase):
    '''For VS 2003 Project File.
    '''
    def parse_file(self, project):
        '''Parse the project file of this particular project instance.
        We do this to find out the dependency of this project on others.
        Return a tuple of the updated project instance, and extra project 
        dependencies (in a dictionary).
        
        project -- an instance of the project     
        '''
        extras = {}
        depends_on = project.depends_on
        
        dom = minidom.parse(self.path)
        
        dom_settings = dom.getElementsByTagName("Settings")[0]
        project.assembly_name = dom_settings.getAttribute("AssemblyName") + ".dll"

        dom_refs = dom.getElementsByTagName("Reference")
        for dom_ref in dom_refs:
            name = dom_ref.getAttribute("Name")
            
            if name not in IGNORE_LIST:
                depends_on.append(name)
                
                if name not in self.projects:
                    new_p = Project(name)
                    new_p.assembly_name = name + ".dll"
                    extras[name] = new_p

        dom.unlink()
        return project, extras

        
class VS2010ProjParser(ProjParserBase):
    def parse_file(self, project):
        '''Parse the project file of this particular project instance.
        We do this to find out the dependency of this project on others.
        Return a tuple of the updated project instance, and extra project 
        dependencies (in a dictionary).
        
        project -- an instance of the project  
        '''
        outputtype_map = {
            'WinExe' : 'exe',
            'Library': 'dll',
        }
        
        extras = {}
        depends_on = project.depends_on
        
        # DEBUG POINT HERE.
        #print self.path        
        dom = minidom.parse(self.path)

        outputtype_key = dom.getElementsByTagName("OutputType")[0].firstChild.nodeValue
        outputtype = outputtype_map[outputtype_key]

        assemblyname = dom.getElementsByTagName("AssemblyName")[0].firstChild.nodeValue
        project.assembly_name = "%s.%s" % (assemblyname, outputtype.lower())
        
        dom_refs = dom.getElementsByTagName("Reference")
        for dom_ref in dom_refs:
            name = dom_ref.getAttribute("Include").split(',')[0]
            
            if name not in IGNORE_LIST:
                depends_on.append(name)
                
                if name not in self.projects:
                    new_p = Project(name)
                    new_p.assembly_name = name + ".dll"
                    extras[name] = new_p

        dom_projrefs = dom.getElementsByTagName("ProjectReference")
        for dom_projref in dom_projrefs:
            name = dom_projref.getElementsByTagName("Name")[0].firstChild.nodeValue
            depends_on.append(name)
                            
        dom.unlink()  
        return project, extras        
   
        
class AssemblyInfoParser:
    '''Parse the AssemblyInfo.cs file to extract assembly information.
    '''
    def __init__(self, path):
        '''Constructor.
        
        path -- a str of the AssemblyInfo.cs path
        '''
        self.path = path

    def parse_file(self, project):
        '''
        
        project --
        '''
        for line in open(self.path, 'r'):
            if line.startswith("[assembly: AssemblyVersion("):
                project.assembly_version = line.split('"')[1]
                break
        return project

        
def get_projects(sln_path):
    '''Make a list of assemblies (nodes) by parsing the
    solution file.
    
    sln_path -- a str of the solution file's path
    '''
    sln_parser = SolutionFileParser(sln_path)
    projects = sln_parser.parse_file()
    return projects


def get_relations(projects, ProjectFileParser):
    '''Make relations (arcs) between assemblies (nodes) 
    by parsing each project file (represented in the
    projects dictionary mapping).
    
    projects -- a dict of name:project (str:obj)
    ProjectFileParser -- a ProjectFileParser class
    '''
    all_projects = {}
    for name, p in projects.iteritems():       
        if not os.path.exists(p.path):
            print "<%s> Project directory not found!  " \
                  "The path is supposed to be <%s>" % (p.name, p.path)
            continue

        proj_parser = ProjectFileParser(p.path, projects)
        p, extras_projects = proj_parser.parse_file(p)
        
        if len(extras_projects) > 0:
            all_projects.update(extras_projects)

        # Get the assembly version number by parsing 
        # the assemblyinfo.cs file.
        asm_path = os.path.join(os.path.dirname(p.path), "assemblyinfo.cs")
        if not os.path.exists(asm_path):
            asm_path = os.path.join(os.path.dirname(p.path), "Properties", "assemblyinfo.cs")
        asm_parser = AssemblyInfoParser(asm_path)
        p = asm_parser.parse_file(p)
        
        projects[name] = p

    all_projects.update(projects)
    return all_projects


def generate_output(projects, output_path):
    '''Call Graphviz here to generate the graph.
    
    projects -- a dict of all projects to be included in the output.
    output_path -- a str of the image output path.
    '''                                        
    graph = pydot.Dot(
        graph_type='digraph', 
        layout='dot',  # dfp
        ratio='0.3',  # may need to tweak this for each graph.
        splines='ortho',
        ranksep='0.5 equally')
    nodes = {}

    id = 0
    for name in projects:
        p = projects[name]
        nodecolor = ""
        while len(nodecolor) != 7:
            nodecolor = "#%s" % hex(random.randrange(0, 0xdddddd))[2:]
        label = p.assembly_name
        # if p.assembly_version != "unknown":
            # label = "%s\\n%s" % (p.assembly_name, p.assembly_version)
        # else:
            # label = p.assembly_name
        node = pydot.Node(label, style="filled", color=nodecolor, shape="box", 
            fontname='Arial', fontsize='12', fontcolor='white')
        graph.add_node(node)
        nodes[name] = node
        id = id + 1

    for name in projects:
        p = projects[name]
        node = nodes[name]
        for head in p.depends_on:
            edge = pydot.Edge(
                node.get_name(), 
                nodes[head].get_name(), 
                color=node.get_color(),
                tooltip="%s depends on %s" % (p.name, head),
                arrowtail="dot")
            graph.add_edge(edge)
    
# For debugging the DOT file.    
#    graph.write_dot(output_path + '.dot', prog='dot')
#    graph.write_svg(output_path + '.svg', prog='dot')
    graph.write_png(output_path + '.png')

def generate_debug(projects):
    '''Generate as text output.  For debugging.
    
    projects -- a dict of all projects to be included in the output.
    '''
    for name in projects:
        p = projects[name]
        print p.assembly_name
        print "  version: %s" % p.assembly_version
        print "  path: %s" % p.path
        
        count = len(p.depends_on)
        if count > 0:
            print "  depends on %s assemblies:" % count
        
        for d in p.depends_on:
            print "    %s" % d

        print ""


def main():
    try:
        num_of_args = len(sys.argv)
        if num_of_args < 1:
            raise UsageError("Wrong number of input arguments!")

        if '-h' in sys.argv or '--help' in sys.argv:
            raise UsageError(USAGE)
      
        sln_path = os.path.abspath(sys.argv[1])            
        
        if not os.path.exists(sln_path):
            raise UsageError("<%s> does not exist!" % sln_path)
        
        projects = get_projects(sln_path)
        proj_parser_class = ParserFactory(sln_path)
        projects = get_relations(projects, proj_parser_class)
        
        if '-d' in sys.argv or '--debug' in sys.argv:
            generate_debug(projects)
        else:
            generate_output(projects, sln_path)

        sys.exit(0)

    except UsageError, err:
        print >> sys.stderr, err.msg
        sys.exit(1)


if __name__ == "__main__":
    main()
