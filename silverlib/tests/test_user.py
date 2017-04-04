from silverlib.user import UserBase, UserManager
from silverlib.objectstores import dirdb

import unittest
import tempfile, shutil


class UserBaseTest(unittest.TestCase):
    
    def testUsage(self):
        password = "abcdefgh"
        name = "Alex"
        u = UserBase(name)
        u.password = password
        
        self.assertEqual(u.check_password(password), True)
        self.assertEqual(u.check_password("wrong password"), False)
        self.assertEqual(u.name, name)
        
        u.password


class UserBaseSubclass(UserBase): pass


class UserManagerTest(unittest.TestCase):
   
    def setUp(self):
        self.path = tempfile.mkdtemp()
        self.mgr = UserManager(dirdb.SimpleDirStore(self.path))
        
    
    def tearDown(self):
        shutil.rmtree(self.path)
        
    
    def testAuthenticateUser(self):
        name = "Alex"
        password = "123456"
        
        u = UserBase(name)
        u.password = password
        self.mgr.set_user(u)
        self.assertEqual(self.mgr.authenticate_user(name, password), True)
        self.assertEqual(self.mgr.authenticate_user("NO", "ONE"), False)
        self.assertEqual(self.mgr.authenticate_user(name, "WRONG"), False)


    def testSetUser(self):
        def set_string():
            self.mgr.set_user("hello world")
        self.assertRaises(TypeError, set_string)
    
        self.mgr.set_user(UserBase("world"))
        self.mgr.set_user(UserBaseSubclass("hello"))
        
    

def main():
    unittest.main()


if __name__ == "__main__":
    main()


