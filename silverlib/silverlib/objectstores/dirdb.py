"""
Using a directory as a database, each entry is a pickle file, where
the name of the pickle file is the key (therefore the pickled object
is the item).  The classes have a dictionary-like interface. 
"""


import os
from silverlib.thirdparty.portalocker import lock, SH, EX

try:
    import cPickle as pickle
except ImportError:
    import pickle
    

class PathNotDirError(Exception):
    pass


class SimpleDirStore(object):
    """
    A simplistic implementation of a persistent database using 
    a filesystem directory.  
    Characteristics: simple but slow.  No extra software needed.
    Should be ok for application with a small load though.
    """

    def __init__(self, path):
        if not os.path.isdir(path):
            raise PathNotDirError('%s is not a directory.' % path)
        self.path = path


    def _check_key_type(self, key):
        if not isinstance(key, basestring):
            raise TypeError("The key '%s' has to be a string "
                            "or unicode instance." % key)

            
    def __setitem__(self, key, value):
        self._check_key_type(key)
        
        f = open(os.path.join(self.path, key), 'w')
        lock(f, EX)
        
        try:
            pickle.dump(value, f, -1)
        finally:
            f.close()


    def __getitem__(self, key):
        self._check_key_type(key)
        
        try:
            f = open(os.path.join(self.path, key), 'r')
            lock(f, SH)
            
            try:
                data = pickle.load(f)
            finally:
                f.close()
        
            return data
        
        except IOError:
            raise KeyError(key)


    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default


    def __delitem__(self, key):
        self._check_key_type(key)
        try:
            os.remove(os.path.join(self.path, key))
        except OSError: # file not found
            pass


    def __len__(self):
        return len(os.listdir(self.path))


    def keys(self):
        return os.listdir(self.path)


    def values(self):
        result = []
        for i in os.listdir(self.path):
             result.append(self[i])
        return result


    def items(self):
        result = []
        for i in os.listdir(self.path):
            result.append((i, self[i]))
        return result


    def __contains__(self, key):
        if key in os.listdir(self.path):
            return True
        return False


    def has_key(self, key):
        return key in self
 


class CachingDirStore(SimpleDirStore):
    """
    A caching persistent storage... minimizing the number of 
    reading a file from the filesystem and unpickling it by 
    saving an instance in the python runtime.
    """
    
    def __init__(self, path):
        SimpleDirStore.__init__(self, path)
        self._cache = {}


    def __setitem__(self, key, value):
        self._check_key_type(key)
        f = open(os.path.join(self.path, key), 'w')
        lock(f, EX)
        
        try:
            pickle.dump(value, f, -1)
        finally:
            f.close()
        
        self._cache[key] = (value, self._get_mtime(key))


    def __getitem__(self, key):
        self._check_key_type(key)
        if key in self._cache:
            value, time = self._cache[key]
            if self._get_mtime(key) == time:
                return value
        try:
            f = open(os.path.join(self.path, key), 'r')
            lock(f, SH)

            try:
                value = pickle.load(f)
            finally:
                f.close()
                
            self._cache[key] = (value, self._get_mtime(key))
            return value
        except IOError:
            raise KeyError(key)
        

    def __delitem__(self, key):
        self._check_key_type(key)
        SimpleDirStore.__delitem__(self, key)
        del self._cache[key]
    
    
    def _get_mtime(self, key):
        path = os.path.join(self.path, key)
        return os.stat(path).st_mtime
 
