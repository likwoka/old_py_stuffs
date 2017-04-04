from silverlib.objectstores.postgresdb import PostgresStore
from silverlib.tests import test_dirdb

import unittest


class PostgresStoreTest(test_dirdb.SimpleDirDBTest):

    def setUp(self):
        self._connstr = "host=;database=;user=;password=;"
        self._tablename = "PosgresStoreUnitTest"
        self._db = PostgresMapping(self._connstr, self._tablename)

    def tearDown(self):
        self._db.close()

    del test_dirdb.SimpleDirDBTest.testPathProblems
    del test_dirdb.SimpleDirDBTest.testDirNotWritable


def main():
    unittest.main()


if __name__ == "__main__":
    main()
    
