from silverlib.dbaccess import generic
import psycopg as dbapi


class ConnectionHelper(generic.ConnectionHelper):
    """
    A Postgresql specific ConnectionHelper class.
    """
    
    def __init__(self, conn_str):
        """
        Constructor.

        conn_str -- a string of connection string.
        """
        connection = dbapi.connect(conn_str,
                                   maxconn=5,
                                   minconn=5,
                                   serialize=0)
        generic.ConnectionHelper.__init__(self, connection)


