import sha


class UserBase(object):
    """
    An user class that would be persisted to a database. 
    
    Attributes:
    name - string, username
    password - string, password
    is_admin - boolean, True means user is an admin
    """
    
    def __init__(self, name):
        self.name = name
        self._password = ""


    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = self._encode(password)

    password = property(_get_password, _set_password)
  
  
    def _encode(self, password):
        """
        Return a hash from a clear text password.
        password - string, a clear text password
        """
        return sha.new(password).hexdigest()
   
   
    def check_password(self, password):
        if not isinstance(password, basestring):
            raise TypeError("password has to be type string or unicode.")

        if self.password == self._encode(password):
            return True
        return False



class UserManager(object):
    """
    A UserManager is responsible for keeping track of User instance.
    In essence, this class contains business rules while the user_mapping
    is the storage technology abstraction.
    """
    
    def __init__(self, user_mapping):
        """
        Constructor.
        
        user_mapping -- an instance of UserDB. 
        """
        self._user_mapping = user_mapping


    def set_user(self, user):
        """
        Put a user into the database.
        
        user -- an instance of UserBase of its subclasses.
                Represent a user.
        """
        if not isinstance(user, UserBase):
            raise TypeError("Value has to be an instance of "
                            "User or its subclasses.")
        self._user_mapping[user.name] = user


    def get_user(self, username, default=None):
        """
        Return an user instance corresponding to
        the username.
        
        username -- a string representing the username.
        """
        return self._user_mapping.get(username, default)


    def __getitem__(self, username):
        return self._user_mapping[username]


    def __delitem__(self, username):
        del self._user_mapping[username]


    def __len__(self):
        return len(self._user_mapping)


    def has_user(self, username):
        """
        Return True if a user with that username is found;
        False otherwise.

        username -- a string representing the username.
        """
        return username in self

    def __contains__(self, username):
        """
        Return True if a user with that username is found;
        False otherwise.

        username -- a string representing the username.
        """
        return self._user_mapping.has_key(username)


    def keys(self):
        """
        Return a list of usernames.
        """
        return self._user_mapping.keys()


    def values(self):
        """
        Return a list of user instances.
        """
        return self._user_mapping.values()


    def items(self):
        """
        Return a list of tuples where the first element
        is the username, and the second element is the 
        user instance.
        """
        return self._user_mapping.items()


    def authenticate_user(self, username, password):
        """
        Return True if username and password match the database entry;
        Return False otherwise.
        """
        user = self.get_user(username, None)
        if user is not None:
            if user.check_password(password):
                return True
        return False


