"""
A RDBMS-independent class for database/SQL handling.
This simplifies Python's DBAPI for convenience.
To use, either pass in a RDBMS specific connection, 
or subclass this class and override the constructor 
__init__().
"""

class ConnectionHelper(object):
    """
    This class simplifies the common usage for a dbapi connection.
    For more complicated usage, for example, transaction, use the 
    connection attribute to return a dbapi connection instead.

    Note that this class is RDBMS-independent, it only depends
    on Python's DBAPI.
    """
    
    def __init__(self, connection):
        """
        Constructor.

        connection -- a dbapi connection instance.
        """
        self.connection = connection
        self.connection.autocommit(True)

    
    def close(self):
        """
        Close the underlying connection.  Once close,
        this ConnectionHelper instance cannot be used.
        """
        self.connection.close()

    
    def __del__(self):
        # Prevent resource leak.
        self.close()


    def _exec(self, sql, *args):
        """
        Return a cursor.  Note that the calling function
        have to explicitly call close() on the returned
        cursor once things are done.

        sql -- a string of the SQL statement.
        args -- a list of arguments to be substituted 
                into the SQL statement.
        """
        cursor = self.connection.cursor()
        cursor.commit()
        if len(args) == 1 and type(args[0]) == dict:
            args = args[0]

        cursor.execute(sql, args)
        return cursor
        

    def exec_none(self, sql, *args):
        """
        Execute the SQL with the arguments.  Return none.
        Use this for query that won't return any data.

        sql -- a string of the SQL statement.
        args -- a list of arguments to be substituted 
                into the SQL statement.
        """
        cursor = self._exec(sql, *args)
        cursor.close()


    def exec_one(self, sql, *args):
        """
        Execute the SQL with the arguments.  Return one value.
        Use this for query that would return exactly one row 
        with just one column.

        sql -- a string of the SQL statement.
        args -- a list of arguments to be substituted 
                into the SQL statement.
        """
        cursor = self._exec(sql, *args)
        result = cursor.fetchone()
        cursor.close()
        return result[0]


    def exec_many(self, sql, *args):
        """
        Execute the SQL with the arguments.  Return a list of list.
        Use this for query that would return many rows.

        sql -- a string of the SQL statement.
        args -- a list of arguments to be substituted 
                into the SQL statement.
        """
        cursor = self._exec(sql, *args)
        result = cursor.fetchall()
        cursor.close()
        return result


