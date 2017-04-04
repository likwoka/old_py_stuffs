"""
TODO Finish this when a database is used.
"""

from silverlib.dbaccess.generic import ConnectionHelper
import unittest

data = [(1, 'hello world', 100, 'yes'),
        (2, 'wow', 200, 'no'),
        (3, 'ha', 400, 'yes'),]


class MockConnection:

    def __init__(self):
        pass


    def autocommit(self, flag):
        pass


    def close(self):
        pass


    def cursor(self):
        return MockCursor()


class MockCursor:
               
    def __init__(self):
        global data
        self.is_closed = False
        self._data = data


    def commit(self):
        pass


    def execute(sql, args):
        pass


    def fetchone(self):
        if not self.is_closed:
            return self._data[0]
        else:
            raise Exception("cursor is closed.")


    def fetchall(self):
        if not self.is_closed:
            return self._data
        else:
            raise Exception("cursor is closed.")


    def close(self):
        self.is_closed = True



class ConnectionHelperTest(unittest.TestCase):
    
    def setUp(self):
        self._conn = ConnectionHelper(MockConnection())


    def tearDown(self):
        self._conn.close()


    def testExecNone(self):
        self._conn.exec_none("")


    def testExecOne(self):
        result = self._conn.exec_one("")


    def testExecMany(self):
        global data
        result = self._conn.exec_many("")
        self.assertEqual(list, type(result))
        self.assertEqual(len(data), len(result))
        

        
def main():
    unittest.main()

if __name__ == "__main__":
    main()

