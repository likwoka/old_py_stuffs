"""
Unittest for session.py.
Note that the global get_request()..etc in Quixote would fail the tests.
"""

from silverlib.quixote.session import SessionBase, \
SlidingTimeoutSessionManager, FixedTimeoutSessionManager, \
remove_dead_session
from silverlib.objectstores.dirdb import CachingDirStore

import unittest, tempfile, shutil


# Magic to make the global get_request() call works.
from quixote import publish

class NullObject:
    def get_environ(self, var):
        return "Hello"

    def get_request(self):
        return self

publish._publisher = NullObject()
# End Magic


class SessionBaseSubclass(SessionBase): pass


class CachingDirNoTimeoutSessionManager(unittest.TestCase):
    
    def testSet(self):
        path = tempfile.mkdtemp()
        db = CachingDirStore(path)

        def set_non_session():
            db["1"] = "Hello World"
###        self.assertRaises(TypeError, set_non_session)
      
        s = SessionBase(12345)
        s.value = "Hello World"
        db["1"] = s

        s2 = db["1"]
        self.assertEqual(s, s2)
        self.assertEqual(s2.value, "Hello World")
        
        db["2"] = SessionBaseSubclass("2")
        
        shutil.rmtree(path)


class SlidingTimeoutSessionManagerTest(unittest.TestCase):
    pass


class FixedTimeoutSessionManagerTest(unittest.TestCase):
    pass


class DeadSessionReaperTest(unittest.TestCase):
    pass
        

def main():
    unittest.main()


if __name__ == "__main__":
    main()

