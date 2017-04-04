"""
Generic INI file handling.
"""

from ConfigParser import RawConfigParser



class IniFile(object):
    """
    A class represents a parsed INI file.
    """

    def __init__(self, schema=None):
        """
        Constructor.

        schema -- A dict of dict of tuple representing 
                  the schema for configuration file.
        """
        self._dict = {}
        self.schema = schema


    def load_from_file(self, path):
        """
        Load the INI file into the instance.

        path -- a string of path to the INI file.
        """
        schema = self.schema
        
        # Set up the default values.
        if schema is not None:
            for sect, sect_obj in schema.items():
                for opt, val in sect_obj.items():
                    # This call is to convert the value to
                    # the type specified.  We do this to
                    # prevent the programmer from specifying
                    # inconsistent type with the value in the 
                    # schema.
                    self.set(*_convert(schema, sect, opt, val[1]))

        # Parse the INI file.
        parser = RawConfigParser()
        parser.read(path)
        
        sections = parser.sections()
        for section in sections:
            
            # If application has supplied a schema,
            # and it does not has such a section, we skip
            # it.  No error raised.
            if schema is not None and \
               not schema.has_key(section):
                continue

            options = parser.options(section)
            
            for option in options:
                
                # If application has supplied a schema,
                # we know the section is valid since it pass the
                # previus test, but if the option is not included
                # in the section, we skip it.  No error raised.
                if schema is not None and \
                   (option not in schema[section]):
                    continue 
                
                # If there is a schema, then we convert the 
                # option to its type stated in the schema,
                # otherwise we just leave it as string.
                if schema is not None:
                    self.set(*_convert(schema, section, option,
                                       parser.get(section, option)))
                else:
                    self.set(section, option,
                             parser.get(section, option))


    def get(self, section, option):
        """
        Return an option in a particular section.  If the 
        option or the section is not found, return None.
        The returned option is a string.

        section -- a string representing the section.
        option -- a string representing the option.
        """
        if self._dict.has_key(section):
            return self._dict[section].get(option, None)
        return None


    def set(self, section, option, value):
        """
        Set an option in a particular section.

        section -- a string representing the section.
        option -- a string representing the option.
        value -- the value.
        """
        if not self._dict.has_key(section):
            self._dict[section] = {}
        
        self._dict[section][option] = value



def _convert(schema, section, option, value):
    """
    Return a tuple of section, option, and value,
    where the section and option are the same as the
    passed in variables, and the value is typed
    according to the schema structure.

    schema -- the application specific configuration
              options structure, a dict of dict of tuple.
    section -- a string of the section the option belongs to.
    option --  a string of the option.
    value -- the value.
    """
    t = schema[section][option][0]
    
    if t == "str":
        result = value
    elif t == "int":
        result = int(value)
    elif t == "float":
        result = float(value)
    elif t == "bool":
        if str(value).upper() in ("1", "TRUE", "YES", "Y"):
            result = True
        elif str(value).upper() in ("0", "FALSE", "NO", "N"):
            result = False
        else:
            raise ValueError("Not a proper boolean value")
    else:
        raise ValueError("option can only be of type "
                         "int, float, str, or bool")
    return section, option, result



def configure(path, schema):
    """
    Return an IniFile instance filled with options from a 
    configuration INI file.  
    
    The schema for the configuration options has this structure:
    
    schema = {
        "section1" : {
            "a" : ("int | float | str | bool", "default value"),
            "b" : ("int | float | str | bool", "default value"),
            },
        "section2" : {
            "a" : ("int | float | str | bool", "default value"),
            "b" : ("int | float | str | bool", "default value"),
            },
        }   
    
    If no schema is given, then all options presented in
    configuration file will be in the returned IniFileOptions 
    instance.  In that case, all option values are string type.
    
    path -- a string representing the INI file path.
    schema -- a dict of dict of tuple representing an 
              application's specific configuration options.
    """

    result = IniFile(schema)
    result.load_from_file(path)
    return result

