"""
%prog [options]

Generate C# class files for parsing AS400 MQ Message from XML defintion file.

examples:
    %prog /path/to/definition.xml 
    %prog -o /path/to/output/directory /path/to/definition.xml
    %prog -v
    %prog -s
    %prog -e 
    %prog -i
    %prog -h
"""

USAGE = __doc__
VERSION = "0.2 (2006 11 10)"


SCHEMA_FILENAME = 'schema.xsd'
EXAMPLE_FILENAME = 'example.xml'


SCHEMA_CONTENT = '''<?xml version="1.0" encoding="UTF-8"?>
<!--Version 0.1-->
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified">
	<xs:element name="def">
		<xs:complexType>
			<xs:sequence>
				<xs:element name="trans" type="transType"/>
				<xs:element name="segments" type="segmentsType"/>
			</xs:sequence>
			<xs:attribute name="namespace" type="xs:string" use="required"/>
		</xs:complexType>
	</xs:element>
	<xs:complexType name="fieldType">
		<xs:simpleContent>
			<xs:extension base="xs:string">
				<xs:attribute name="name" type="xs:string" use="required"/>
				<xs:attribute name="type" use="required">
					<xs:simpleType>
						<xs:restriction base="xs:NMTOKEN">
							<xs:enumeration value="a"/>
							<xs:enumeration value="d72"/>
							<xs:enumeration value="dt"/>
							<xs:enumeration value="i"/>
						</xs:restriction>
					</xs:simpleType>
				</xs:attribute>
				<xs:attribute name="length" use="required" type="xs:int"/>
				<xs:attribute name="format">
					<xs:simpleType>
						<xs:restriction base="xs:NMTOKEN">
							<xs:enumeration value="hhmmss"/>
							<xs:enumeration value="yyyyMMdd"/>
						</xs:restriction>
					</xs:simpleType>
				</xs:attribute>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
	<xs:complexType name="segType">
		<xs:attribute name="name" use="required" type="xs:string"/>
		<xs:attribute name="count" use="required">
			<xs:simpleType>
				<xs:restriction base="xs:NMTOKEN">
					<xs:enumeration value="one"/>
					<xs:enumeration value="many"/>
				</xs:restriction>
			</xs:simpleType>
		</xs:attribute>
	</xs:complexType>
	<xs:complexType name="segmentType">
		<xs:sequence>
			<xs:element name="field" type="fieldType" maxOccurs="unbounded"/>
		</xs:sequence>
		<xs:attribute name="name" use="required" type="xs:string"/>
	</xs:complexType>
	<xs:complexType name="segmentsType">
		<xs:sequence>
			<xs:element name="segment" type="segmentType" maxOccurs="unbounded"/>
		</xs:sequence>
	</xs:complexType>
	<xs:complexType name="tranType">
		<xs:sequence>
			<xs:element name="seg" type="segType" maxOccurs="unbounded"/>
		</xs:sequence>
		<xs:attribute name="name" use="required" type="xs:string"/>
	</xs:complexType>
	<xs:complexType name="transType">
		<xs:sequence>
			<xs:element name="tran" type="tranType" maxOccurs="unbounded"/>
		</xs:sequence>
	</xs:complexType>
</xs:schema>
'''

EXAMPLE_CONTENT = '''<?xml version="1.0" encoding="UTF-8"?>
<def namespace="RBFG.Insurance.YJT0.DataParsing"> 
	<!-- count is either one or many; many becomes a list -->
	<trans>
		<tran name="WQ222Request">
			<seg name="WQ222Header" count="one"/>
			<seg name="ActivationStatusRequest" count="many"/>
			<seg name="MessageEndSegment" count="one"/>
		</tran>
		<tran name="WQ222Response">
			<seg name="WQ222Header" count="one"/>
			<seg name="ActivationStatusResponse" count="many"/>
			<seg name="MessageEndSegment" count="one"/>
		</tran>
	</trans>
	<!-- type: a for alpha, i for integer, dt for datetime, d72 for decimal in 7.2 format -->
	<!-- use the format attribute for dt only -->
	<segments>
		<segment name="WQ222Header">
			<field name="Request Code" type="a" length="3">222</field>
			<field name="Web UID" type="a" length="32"/>
			<field name="Date" type="dt" format="yyyyMMdd" length="8"/>
			<field name="Time" type="dt" format="hhmmss" length="6"/>
			<field name="Return Code" type="a" length="3"/>
		</segment>
		<segment name="ActivationStatusRequest">
			<field name="Label" type="a" length="6">@@ASRQ</field>
			<field name="Activation Code" type="a" length="10"/>
			<field name="End Segment" type="a" length="1">|</field>
		</segment>
		<segment name="MessageEndSegment">
			<field name="Label" type="a" length="6">@@ENDM</field>
			<field name="End Segment" type="a" length="1">|</field>
		</segment>
		<segment name="ActivationStatusResponse">
			<field name="Label" type="a" length="6">@@ASRP</field>
			<field name="Activation Code" type="a" length="10"/>
			<field name="Return Code" type="a" length="3"/>
			<field name="Activation Status" type="a" length="1"/>
			<field name="Policy Number" type="a" length="11"/>
			<field name="Expiry Date" type="dt" format="yyyyMMdd" length="8"/>
			<field name="Transaction Number" type="i" length="5"/>
			<field name="Effective Date" type="dt" format="yyyyMMdd" length="8"/>
			<field name="Effective Time" type="dt" format="hhmmss" length="6"/>
			<field name="Transaction Effective Date" type="dt" format="yyyyMMdd" length="8"/>
			<field name="Transaction Expiry Date" type="dt" format="yyyyMMdd" length="8"/>
			<field name="Line of Business" type="a" length="1"/>
			<field name="Annual Discounted Premium" type="d72" length="9"/>
			<field name="Policy Status" type="a" length="1"/>
			<field name="Policy Holder 1 Last Name" type="a" length="30"/>
			<field name="Policy Holder 1 First Name" type="a" length="30"/>
			<field name="Policy Holder 2 Last Name" type="a" length="30"/>
			<field name="Policy Holder 2 First Name" type="a" length="30"/>
			<field name="Date of Birth" type="dt" format="yyyyMMdd" length="8"/>
			<field name="Plan Code" type="a" length="8"/>
			<field name="Policy Term" type="a" length="3"/>
			<field name="Transaction Premium Sign" type="a" length="1"/>
			<field name="Transaction Premium" type="d72" length="9"/>
			<field name="Written Premium" type="d72" length="9"/>
			<field name="TH Quote Policy Number" type="a" length="8"/>
			<field name="End Segment" type="a" length="1">|</field>
		</segment>
	</segments>
</def>
'''

# -----------------------------------------------------------------------------

# substitute: namespace, classname, addsegment_list, segment_list
TRAN_CLASS_TEMPLATE = '''// Do not edit!  This file is auto-generated.
using System;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace ${namespace} 
{
	public class ${classname} : Tran
	{

		public ${classname}()
		{
            ${addsegment_list}
		}


		public static ${classname} ToObject(IState state)
		{		
			${classname} tran = new ${classname}();
			${classname} result = new ${classname}();

			int max = tran.Segments.Count;
			for (int i = 0; i < max; i++)
			{
				state = (tran.Segments[i]).ToObject(state);
				result.Segments[i] = state.Output as ISegment;
			}
		
			return result;
		}

        
        ${segment_list}
    }
}
'''

# substitute: namespace, classname 
SEGMENTLIST_CLASS_TEMPLATE = '''// Do not edit!  This file is auto-generated. 
using System;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace ${namespace}
{

    public class ${classname}List : SegmentList
	{
		
		public ${classname} this[int index]
		{
			get
			{
				return List[index] as ${classname};
			}
			set
			{
				List[index] = value;
			}
		}


		public override IState ToObject(IState state)
		{	
			Segment segment = new ${classname}();
			string input = state.Input;
			int pos = state.StartPos;
			int end = input.Length;
			int length = segment.Fields[0].Length;
			
			while (pos < end)
			{
				string label = input.Substring(pos, length);
				
				if (segment.Fields[0].String == label)
				{
					segment = new ${classname}();
					state = segment.ToObject(state);
					List.Add(state.Output);
					pos = state.StartPos;
				}
				else
				{
					break;
				}
			}
			
			state.Output = this;			
			return state;
		}
	}
}
'''

# substitute: namespace, classname, addfield_list, field_list
SEGMENT_CLASS_TEMPLATE = '''// Do not edit!  This file is auto-generated. 
using System;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace ${namespace}
{
	public class ${classname} : Segment
	{
		public ${classname}()
		{
            ${addfield_list}
		}

        ${field_list}
	}	
}
'''

# substitute: namespace
PARSESTATE_CLASS_TEMPLATE = '''// Do not edit!  This file is auto-generated. 
using System;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace ${namespace}
{

	public class State : IState
	{
		public State(string input, int startPos)
		{
			_input = input;
			_startPos = startPos;
		}


		public State(string input) : this(input, 0) {}


		public string Input
		{
			get
			{
				return _input;
			}
			set
			{
				_input = value;
			}
		}


		public object Output
		{
			get
			{
				return _output;
			}
			set
			{
				_output = value;
			}
		}


		public int StartPos
		{
			get
			{
				return _startPos;
			}
			set
			{
				_startPos = value;
			}
		}


		private string _input;
		private int _startPos;
		private object _output;
	}
}
'''

# substitute: segmentname
SEGMENT_TEMPLATE = '''
 		public ${segmentname} ${segmentname}
		{
			get
			{
				return Segments["${segmentname}"] as ${segmentname};
			}
			set
			{
				${segmentname} = value;
			}
		}

'''

# substitute: cstype, type, fieldname
FIELD_TEMPLATE = '''
        public ${cstype} ${fieldname}
        {
            get
            {
                return Fields["${fieldname}"].${type};
            }
            set
            {
                Fields["${fieldname}"].${type} = value;
            }
        }

'''

# substitute: fieldname, fieldtype, fieldlength, fielddefault
ADDFIELD_TEMPLATE = '''
            Fields.Add("${fieldname}", new Field(${fieldtype}, ${fieldlength}${fielddefault})); 
'''


# substitute: segmentname
ADDSEGMENT_TEMPLATE = '''
            Segments.Add("${segmentname}", new ${segmentname}()); 
'''


# -----------------------------------------------------------------------------
import os, sys, shutil, time, optparse, tempfile, string
from string import Template
from xml.dom.minidom import parse
 

def get_type_tuple(t):
    '''
    Return a tuple of (FieldType, C# Type) according to the
    type attribute in the XML definition in <field>.

    t -- a string of field type used in the XML Definition.
    '''
    types = {'a'   : ('FT.Alpha',     'String',   'string'),
             'dt'  : ('FT.DateTime',  'DateTime', 'DateTime'),
             'd72' : ('FT.Decimal72', 'Decimal',  'Decimal'),
             'i'   : ('FT.Integer',   'Integer',  'int'),}
    try:
        return types[t]
    except KeyError:
        raise Exception("Type '%s' not found!" % t)


def validate_xml(def_file):
    '''
    Valiate the given XML definition file against the schema.
    Note that the schema is embedded in this source, not given 
    from user!
    '''
    try:
        from lxml import etree
    except ImportError:
        print "Need to install lxml and lxml python binding in " \
              "order to validate the XML definition file.  " \
              "The XML parsing and code generation may fail in " \
              "mysterious ways if the XML definition is invalid." \
              "  For more info on lxml and lxml python binding, " \
              "please go to google.com."

    else:
        xmlschema = etree.XMLSchema(etree.parse(SCHEMA_CONTENT))
        
        if xmlschema.validate(def_file):
            print "Definition file is valid according to schema."
        else:
            print "Invalid definition!"
            print xmlschema.error_log


_translation_table = string.maketrans('', '')

def filter_name(orig_name):
    '''
    Filter out characters that are not allowed in
    a C# class name or variable name.
    '''
    ascii_name = orig_name.encode('ascii')

    if " " in ascii_name:
        ascii_name = ascii_name.title()

    name = ascii_name.translate(
            _translation_table,
            string.whitespace + string.punctuation)
    
    if name[0] in string.digits:
        name = "_" + name
    
    return name


def generate_file(filepath, content):
    '''
    Generate a file with the given filename and content.
    
    filepath -- a string of the path to the file (including the filename).
    content -- a string of the file content. 
    '''
    filename = os.path.basename(filepath)

    if os.path.exists(filepath):
        while 1:
            is_overwrite = raw_input("There is already a file called '%s' "
            "in this directory, do you want to overwrite it? (y/n)\n" % filename)
            
            if is_overwrite.lower() == 'n':
                print "Ok, aborting.  Please rename the existing file '%s' " \
                "to something else first.  Then run this command again." % filename
                sys.exit(1) # raise SystemExit
            
            elif is_overwrite.lower() == 'y':
                os.remove(filepath)
                write_out(filepath, content)
                print "Done.  The file is created at %s" % filepath
                break
            else:
                print "Huh!?  Don't understand, please answer with either y or n."
    
    else:
        write_out(filepath, content)


def write_out(path, content):
    '''
    Write the content to the path given.
    '''
    f = tempfile.TemporaryFile(dir=os.path.dirname(path))
    tmp_path = f.name
    f.close()
    tmp_file = open(tmp_path, 'w+b')
    tmp_file.write(content)
    tmp_file.close()
    os.rename(tmp_path, path)
 

def get_csharp_path(dirname, classname):
    '''
    Return the full path of the given classname for class file generation.
    '''
    return os.path.join(dirname, classname + '.cs')


def make_classes(def_path, output_dir):
    '''
    Parse the XML definition file, then create the class files.
    '''
    print "Validating..."
    validate_xml(def_path)

    print "Parsing..."
    dom = parse(def_path)
    namespace = dom.documentElement.getAttribute("namespace")

    # Create Transaction classes.
    tran_nodes = dom.getElementsByTagName("tran")
    for tran_node in tran_nodes:
        
        addsegment_list = []
        segment_list    = []

        seg_nodes = tran_node.getElementsByTagName('seg')
        for seg_node in seg_nodes:
            
            segmentname = filter_name(seg_node.getAttribute('name'))
            
            if seg_node.getAttribute('count') == 'many':
                c = Template(SEGMENTLIST_CLASS_TEMPLATE).substitute(
                        namespace=namespace,
                        classname=segmentname)

                segmentname += 'List'
                
                print "Writing %s.cs ... " % segmentname
                generate_file(get_csharp_path(output_dir, segmentname), c)

            segment_list.append(
                    Template(SEGMENT_TEMPLATE).substitute(
                        segmentname=segmentname))
            addsegment_list.append(
                    Template(ADDSEGMENT_TEMPLATE).substitute(
                        segmentname=segmentname))

        classname       = filter_name(tran_node.getAttribute('name'))
        addsegment_list = '\n'.join(addsegment_list)
        segment_list    = '\n'.join(segment_list)

        c = Template(TRAN_CLASS_TEMPLATE).substitute(
                namespace=namespace,
                classname=classname,
                addsegment_list=addsegment_list,
                segment_list=segment_list)

        print "Writing %s.cs ... " % classname
        generate_file(get_csharp_path(output_dir, classname), c)


    # Create Segment classes.
    segment_nodes = dom.getElementsByTagName("segment")
    for segment_node in segment_nodes:
        
        field_list    = []
        addfield_list = []

        field_nodes = segment_node.getElementsByTagName("field")
        for field_node in field_nodes:
            
            name   = filter_name(field_node.getAttribute("name"))
            t      = get_type_tuple(field_node.getAttribute("type"))
            length = field_node.getAttribute("length")
            format = field_node.getAttribute("format")
            
            text_node = field_node.firstChild
            if text_node is not None:
                default = ', "%s"' % text_node.nodeValue
            else:
                default = ''

            field_list.append(
                Template(FIELD_TEMPLATE).substitute(
                    cstype=t[2],
                    type=t[1],
                    fieldname=name))
                
            fieldtype = t[0]
            if fieldtype == 'FT.DateTime':
                fieldtype = '%s, "%s"' % (fieldtype, field_node.getAttribute("format"))

            addfield_list.append(
                Template(ADDFIELD_TEMPLATE).substitute(
                    fieldname=name,
                    fieldtype=fieldtype,
                    fieldlength=length,
                    fielddefault=default))

        classname     = filter_name(segment_node.getAttribute("name"))
        field_list    = '\n'.join(field_list)
        addfield_list = '\n'.join(addfield_list)
        
        c = Template(SEGMENT_CLASS_TEMPLATE).substitute(
                namespace=namespace,
                classname=classname,
                field_list=field_list,
                addfield_list=addfield_list)
    
        print "Writing %s.cs ... " % classname
        generate_file(get_csharp_path(output_dir, classname), c)
    

    # Create ParseState class.
    c = Template(PARSESTATE_CLASS_TEMPLATE).substitute(namespace=namespace)
    print "Writing State.cs ... "
    generate_file(get_csharp_path(output_dir, "State"), c)

    print 'Done.'
 


def main():
    parser = optparse.OptionParser(USAGE)
    parser.add_option('-e', '--example', action='store_true', help='Generate a sample XML definition file and the corresponding XML schema.')
    parser.add_option('-s', '--schema',  action='store_true', help='Generate the XML schema.')
    parser.add_option('-i', '--version', action='store_true', help='Display the version info')
    parser.add_option('-v', '--validate',help='Validate the XML definition file.')
    parser.add_option('-o', '--output',  help='Specify the output directory.')
    options, args = parser.parse_args()

    if options.version:
        print VERSION
        sys.exit(0)
    
    elif options.example:
        root_dir = os.getcwd()
        print "Generating schema file..."
        generate_file(os.path.join(root_dir, SCHEMA_FILENAME), SCHEMA_CONTENT)
        print "Generating example file..."
        generate_file(os.path.join(root_dir, EXAMPLE_FILENAME), EXAMPLE_CONTENT)
        print "Done."
        sys.exit(0)

    elif options.schema:
        root_dir = os.getcwd()
        print "Generating schema file ..."
        generate_file(os.path.join(root_dir, SCHEMA_FILENAME), SCHEMA_CONTENT)
        print "Done."
        sys.exit(0)

    elif options.validate:
        def_path = os.path.abspath(options.validate)
        validate_xml(def_path)
        sys.exit(0)

    if options.output:
        output_dir = os.path.abspath(options.output)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    else:
        output_dir = os.getcwd()

    if len(args) > 1:
        raise parser.error("Too many arguments!  We just need one!")
    elif len(args) < 1:
        raise parser.error("We need one argument for the XML definition file!")
    else:
        def_path = os.path.abspath(args[0])
        
        if not os.path.exists(def_path):
            raise Exception("%s does not exist!" % def_path)

        make_classes(def_path, output_dir)
        sys.exit(0)
   

if __name__ == "__main__":
    main()

