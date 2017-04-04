"""
Unittest for dirdb.py
"""


from silverlib.objectstores.dirdb import SimpleDirStore, \
CachingDirStore, PathNotDirError

import unittest
import tempfile, shutil, os, stat, sets


class SimpleDirDBTest(unittest.TestCase):
    """
    Test SimpleDirDB.
    """
    
    _DBClass = SimpleDirStore
    
    def setUp(self):
        self._path = tempfile.mkdtemp()
        self._db = self._DBClass(self._path)


    def tearDown(self):
        shutil.rmtree(self._path)

 
    def testPathProblems(self):
        """
        1) Path not exists
        2) Path is not a directory
        Both cases should produce a PathNotDirError.
        """
        def path_not_exist():
            db = self._DBClass("/I/d/o/n/t/e/x/i/s/t")
         
        def path_not_dir():
            dummy, path = tempfile.mkstemp()
            db = self._DBClass(path)
       
        self.assertRaises(PathNotDirError, path_not_exist)
        self.assertRaises(PathNotDirError, path_not_dir)
        
        
    def testDirNotWritable(self):
        """
        1) Directory is not writable
        This should produce an IOError.
        """
        def insert_entry(path):
            db = self._DBClass(path)
            db['test'] = "hello world"
            
        path = tempfile.mkdtemp()
        
        # Set the mode to read only (not writable)
        os.chmod(path, stat.S_IRUSR)
        
        self.assertRaises(IOError, insert_entry, path)

        # Reset the mode to writable so that we can delete it.
        os.chmod(path, stat.S_IRWXU)
        shutil.rmtree(path)
        
        
    def testGetSet(self):
        self._db["test1"] = "Hello World"
        self.assertEqual(self._db["test1"], "Hello World")
        self.assertEqual(self._db.get("test1", None), "Hello World")
        self.assertEqual(self._db.get("notexists", None), None)


    def testLen(self):
        self.assertEqual(len(self._db), 0)
        
        self._db["1"] = "this is 1"
        self.assertEqual(len(self._db), 1)

        self._db["2"] = "This is 2"
        self.assertEqual(len(self._db), 2)

        self._db["2"] = "This is a new 2"
        self.assertEqual(len(self._db), 2)

        del self._db["1"]
        self.assertEqual(len(self._db), 1)
        

    def testHasKey(self):
        self.assertEqual(self._db.has_key("1"), False)
        self._db["1"] = "This is 1"
        self.assertEqual(self._db.has_key("1"), True)
        self.assertEqual(self._db.has_key("2"), False)
       

    def testKeysValuesItems(self):
        testdata = {"1" : "This is 1",
                    "2" : 34567,
                    "3" : "This is 3",}
        
        for key, value in testdata.items():
            self._db[key] = value
 
        self.assertEqual(sets.Set(testdata.keys()),
                         sets.Set(self._db.keys()))

        self.assertEqual(sets.Set(testdata.values()),
                         sets.Set(self._db.values()))

        for key, value in self._db.items():
            self.assertEqual(testdata[key], value)


class CachingDirDBTest(SimpleDirDBTest):
    
    _DBClass = CachingDirStore


def main():
    unittest.main()


if __name__ == "__main__":
    main()


