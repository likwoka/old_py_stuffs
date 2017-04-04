webapplib
=========
A python library package containing reusable components for building
web application in Quixote.


File Overview
-------------
configuration.py -- A configuration module for reading configuration file.
                    Configuration file is a python source file with variables
                    in UPPER CASE.

dirdb.py -- Contains the Directory (folder) Mapping classes.  Mapping is a 
            dict like interface.  The object stored is serialized into a
            file system file.

postgresdb.py -- Contains the Postgresql Mapping class.  The object stored is
                 serialized into a binary in a database table.

publish.py -- A utf-8 session-aware object publisher for use in the Quixote framework.

session.py -- 

user.py -- 


Missing functionality:
1) logging (FileLogger? PostgresLogger?)
2) caching (Cache, a per process in memory cache, validate by?)


Quixote dependent modules
-------------------------
configuration.py
publish.py
session.py


###

This file serves as documentation.  It is not being used 
by any code.


class IUser:
    self.name = None
    self.password = None
    def __init__(self): pass
    def check_password(self, password): return False

class IUserMapping:
    def __init__(self, connection_string): pass
    def __setitem__(self, key, value): pass
    def __getitem__(self, key): return None
    def get_user(self, key, default=None): pass
    def __delitem__(self, key): pass
    def __len__(self): return 0
    def has_user(self, key): return False
    def keys(self): return []
    def values(self): return []
    def items(self): return []

class IUserManager:
    def __init__(self, user_db): pass
    def __setitem__(self, username, value): pass
    def __getitem__(self, username): return None
    def get_user(self, username, default=None): pass
    def __delitem__(self, username): pass
    def __len__(self): return 0
    def has_user(self, username): return False
    def keys(self): return []
    def values(self): return []
    def items(self): return []
    def authenticate_user(self, username, password): return False

class ISession: pass
class ISessionManager: pass
class ISessionMapping: pass

