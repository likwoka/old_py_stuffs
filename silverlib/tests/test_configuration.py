from silverlib.configuration import IniFile

import unittest
import tempfile, os


content = """
[system]
# A sample comment
; in another form
os = windows

# Another sample comment
; in another form
[server]
thread = 10
speed = 300.35
is_ssl = no
is_ssl2 = n
is_ssl3 = false
is_ssl4 = FaLSe
is_http = yes
is_http2 = y
is_http3 = true
is_http4 = TRuE

[app]
greeting = hello, how are you doing?
"""

full_schema = {"system" : {"os" : ("str", ""),},
               "server" : {"thread" : ("int", 1),
                           "speed" : ("float", 0.0),
                           "is_ssl" : ("bool", False),
                           "is_ssl2" : ("bool", False),
                           "is_ssl3" : ("bool", False),
                           "is_ssl4" : ("bool", False),
                           "is_http" : ("bool", True),
                           "is_http2" : ("bool", True),
                           "is_http3" : ("bool", True),
                           "is_http4" : ("bool", True),},
                "app" : {"greeting" : ("str", ""),},}


partial_schema = {"system" : {"os" : ("str", ""),},
                  "server" : {"thread" : ("int", 1),
                              "speed" : ("float", 0.0),
                              "is_ssl" : ("bool", False),}}
 

invalid_schema = {"system" : {"os" : ("string", "")}}


class IniFileTest(unittest.TestCase):

    def setUp(self):
        global content
        (dummy, path) = tempfile.mkstemp()
        f = open(path, 'w')
        f.write(content)
        f.close()
        self.path = path
        self.inifile = None


    def tearDown(self):
        os.remove(self.path)


    def testLoadWithoutSchema(self):
        self.inifile = IniFile()
        self.inifile.load_from_file(self.path)
        
        
    def testLoadWithInvalidSchema(self):
        global invalid_schema
        schema = invalid_schema
        self.inifile = IniFile(schema)
        def load_invalid_schema():
            self.inifile.load_from_file(self.path)
        self.assertRaises(ValueError, load_invalid_schema)


    def testLoadWithFullSchema(self):
        global full_schema
        schema = full_schema
        self.inifile = IniFile(schema)
        self.inifile.load_from_file(self.path)


    def testLoadWithPartialSchema(self):
        global partial_schema
        schema = partial_schema
        self.inifile = IniFile(schema)
        self.inifile.load_from_file(self.path)
        
        
    def testGetWithOutSchema(self):
        self.testLoadWithoutSchema()
        self.assertEqual("windows", self.inifile.get("system", "os"))
        self.assertEqual(None, self.inifile.get("system", "Not Exist"))
        self.assertEqual("10", self.inifile.get("server", "thread"))
        self.assertEqual("300.35", self.inifile.get("server", "speed"))
        self.assertEqual("no", self.inifile.get("server", "is_ssl"))


    def testGetWithPartialSchema(self):
        self.testLoadWithPartialSchema()
        self.assertEqual("windows", self.inifile.get("system", "os"))
        self.assertEqual(None, self.inifile.get("system", "Not Exist"))
        self.assertEqual(10, self.inifile.get("server", "thread"))
        self.assertEqual(300.35, self.inifile.get("server", "speed"))
        self.assertEqual(False, self.inifile.get("server", "is_ssl"))
        self.assertEqual(None, self.inifile.get("server", "is_ssl2"))
    
   
    def testGetWithFullSchema(self):
        self.testLoadWithFullSchema()
        self.assertEqual("windows", self.inifile.get("system", "os"))
        self.assertEqual(None, self.inifile.get("system", "Not Exist"))
        self.assertEqual(10, self.inifile.get("server", "thread"))
        self.assertEqual(300.35, self.inifile.get("server", "speed"))
        self.assertEqual(False, self.inifile.get("server", "is_ssl"))
        self.assertEqual(False, self.inifile.get("server", "is_ssl2"))
        self.assertEqual(False, self.inifile.get("server", "is_ssl3"))
        self.assertEqual(False, self.inifile.get("server", "is_ssl4"))
        self.assertEqual(True, self.inifile.get("server", "is_http"))
        self.assertEqual(True, self.inifile.get("server", "is_http2"))
        self.assertEqual(True, self.inifile.get("server", "is_http3"))
        self.assertEqual(True, self.inifile.get("server", "is_http4"))
        self.assertEqual("hello, how are you doing?",
                         self.inifile.get("app", "greeting"))
        self.assertEqual(None, self.inifile.get("not", "exists"))

        
def main():
    unittest.main()


if __name__ == "__main__":
    main()
 
