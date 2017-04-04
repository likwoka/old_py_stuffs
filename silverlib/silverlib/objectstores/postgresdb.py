"""
Using Postgresql as the backend of a mapping object.
Advantage includes persistence, ACIDity.
Disadvantage includes dependency on an external database and
python-database driver, and more complicated setup.

Requires the python package psycopg in order to work.
"""


import cPickle as pickle
from silverlib.dbaccess.postgres import ConnectionHelper


class SqlStatements:
    """
    This class contains the SQL statement.
    """
    
    def __init__(table_name):
        """
        Constructor.

        table_name -- a string representing the table we want to
                      store stuff in.
        """
        self.create_table = ("create table %s("
                             "key varchar primary key,"
                             "val bytea not null)" % table_name)
        
        self.length = ("select count(key) from %s" % table_name)
        
        self.keys = ("select key from %s order by key asc;"
                     % table_name)
        
        self.values = ("select val from %s order by key asc;" 
                       % table_name)
        
        self.items = ("select key, val from %s order by key asc;" 
                      % table_name)
        
        self.has_key = ("select key from %s where key = %s;" 
                        % (table_name, "%s"))
        
        self.delete = ("delete from %s where key = %s;"
                       % (table_name, "%s"))
        
        self.get = ("select val from %s where key = %s;" 
                    % (table_name, "%s"))
        
        self.set1 = self.delete
        self.set2 = ("insert into %s(key, val) values(%s, %s);" 
                     % (table_name, "%s", "%s"))



class PostgresStore(object):
    """
    This class provides a mapping implemented in a Postgres database.
    """
    
    def __init__(self, conn_str, table_name):
        """
        Constructor.
        
        conn_str -- a string representing the connection string.
        table_name -- a string representing the table we want to
                      store stuff in.
        """
        self.conn_str = conn_str
        self._conn = ConnectionHelper(conn_str)

        self.table_name = table_name
        self._sql = SqlStatements(table_name)

        self._try_create_table()
        
    
    def _try_create_table():
        """
        Try to create the table, and ignore any error if it 
        already exists.
        """
        try:
            self._conn.exec_none(self._sql.create_table)
        except DatabaseError:
            # Most likely table already exists.
            pass


    def __setitem__(self, key, value):
        """
        Serialize an object of value and save it to the key.
        
        key -- a string representing the key.
        value -- an object to be serialized.
        """
        serialized = pickle.dumps(value, -1)
        self._conn.exec_none(self._sql.set1, key)
        self._conn.exec_none(self._sql.set2, key,
                             dbapi.Binary(serialized))


    def __getitem__(self, key):
        """
        Return the value according to the key.
        If the key is not found, it raises a KeyError.
        
        key -- a string representing the key.
        """
        data = self._conn.exec_one(self._sql.get, key)
        try:
            result = pickle.loads(data)
        except EOFError:
            raise KeyError(key)
        return result


    def get(self, key, default=None):
        """
        Return the value according to the key.  If the
        key is not found, return default.

        key -- a string represents the key
        default -- optional, the default value.
        """
        try:
            return self[key]
        except KeyError:
            return default


    def __delitem__(self, key):
        """
        Delete the value according to the key.  Note that
        no error will be raised if the key is not found.
        """
        self._conn.exec_none(self._sql.delete, key)
        

    def __len__(self):
        """
        Return the number of records in the mapping.
        """
        return self._conn.exec_one(self._sql.length)

        
    def keys(self):
        """
        Return a list of all keys in this mapping.
        """
        rows = self._conn.execute_many(self._sql.keys)
        return [row[0] for row in rows]

    
    def values(self):
        """
        Return a list of all values in this mapping.
        """
        rows = self._conn.execute_many(self._sql.values)
        result = []
        for row in rows:
            result.append(pickle.loads(row[0]))
        return result

    
    def items(self):
        """
        Return a list of tuples of key and value in this
        mapping.
        """
        rows = self._conn.execute_many(self._sql.items)
        result = []
        for row in rows:
            result.append((row[0], pickle.loads(row[1])))
        return result


    def __contains__(self, key):
        """
        Does this key exists in this mapping?  
        Return True if it exists, False otherwise.
        
        key -- a string representing the key
        """
        data = self._conn.exec_one(self._sql.has_key, key)
        if data is None:
            return False
        return True
     

    def has_key(self, key):
        """
        Does this key exists in this mapping?  
        Return True if it exists, False otherwise.
        
        key -- a string representing the key
        """
        return key in self
    
     
    def close():
        """
        Close the database connection.  Once close is called,
        this mapping cannot be used.
        """
        self._conn.close()


