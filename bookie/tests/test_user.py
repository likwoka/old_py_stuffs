from bookie.user import User

import unittest


class UserTest(unittest.TestCase):
    
    def testPassword(self):
        password = "abcedfgh"
        u = User("alex")
        u.password = password
        self.assertNotEqual(u.password, password)
        self.assertEqual(u.check_password(password), True)
        self.assertEqual(u.check_password("Wrong"), False)

    
    def testIsAdmin(self):
        u = User("alex")
        self.assertEqual(u.is_admin, False)
        
        u.is_admin = True
        self.assertEqual(u.is_admin, True)
        
        
    def testName(self):
        name = "Alex"
        u = User(name)
        self.assertEqual(u.name, name)

        name2 = "adam"
        u.name = name2
        self.assertEqual(u.name, name2)
        
        
def main():
    unittest.main()


if __name__ == "__main__":
    main()
    
