from quixote import session
from time import time, sleep

try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading


class SessionBase(session.Session):
    """
    A base class for a session object.  Typically you will
    use this class by subclassing it and setting its class
    attribute properties to a list of string.
    
    Example
    =======
    class MySession(SessionBase):
        persistent_properties = ["user", "server_ip", "age"]
    
    Other attributes
    ================
    id -- int, the session id of this session.
    user -- string, the current username the user logged in as.

    Note
    ====
    has_info() -- If True, saves this session.  If False
                  discards it..
    is_dirty() -- This session is already in the SessionManager.
                  Should we need to update the session (write
                  it to the SessionManager again)?
                  If True, yes.  If False, no.
    """

    # A list of string representing the session class's attribute,
    # which when set, should be persisted to the store.
    persistent_properties = []
    
    def __init__(self, id):
        """
        Constructor.
        
        request -- an instance of Quixote.http_request.HTTPRequest
                   object.  The current request we are dealing with.
        id -- an int of the session id.
        """
        session.Session.__init__(self, id)
         
        if "user" not in self.persistent_properties:
            self.persistent_properties.append("user")

        self.user = None

        if "_slidingtimeout_access_time" not in self.persistent_properties:
            self.persistent_properties.append("_slidingtimeout_access_time")
            self._slidingtimeout_access_time = time()
    
        # _dirty flag.  If set to True, the session would be
        # saved to the store.  Otherwise, the session would
        # not be saved to the store.
        self._dirty = False


    def is_dirty(self):
        """
        Return True to written the session to a persistent storage.
        Return False otherwise.
        """
        if self._dirty:
            self._dirty = False
            return True
        return False


    def __setattr__(self, name, value):
        """
        Set attribute method, as in session.x = y, where x is the name,
        y is the value.  If the name is in the list of properties, then
        the dirty flag is set, which means the session has changed and
        should be saved/persisted to the store.

        name -- a string representing the attribute.
        value -- an object.
        """
        if name in self.persistent_properties:
            setattr(session.Session, "_dirty", True)
        setattr(session.Session, name, value)
 
 
        
class NoTimeoutSessionManager(session.SessionManager):
    """
    The "default" session manager.  Session would live
    forever, no timeout.
    """
    def __init__(self, session_class, session_mapping):
        session.SessionManager.__init__(self,
                                        session_class,
                                        session_mapping)

        
    def __setitem__(self, id, session):
        """
        Store a session into the session manager.

        id -- a string of session_id
        session -- an instance of SessionBase or its subclasses.
        """
        if not isinstance(session, SessionBase):
            raise TypeError("Value has to be an instance of "
                            "Session or its subclasses.")
        session.SessionManager.__setitem__(self, id, session)



class SlidingTimeoutSessionManager(NoTimeoutSessionManager):
    """
    Provides a sliding timeout capability.  What this means is
    that the session will timeout after a certain period of 
    inactivity since the last request.
    """
    
    timeout_in_min = 30


    def is_session_timedout(self, session_obj):
        """
        Return True if session has timed out, False otherwise.

        session_obj -- an instance of SessionBase or its subclass.
        """
        now = time()
        sec_since_last_access = now - \
                session_obj._slidingtimeout_access_time
        
        if sec_since_last_access >= self.timeout_in_min * 60:
            return True
        else:
            return False

            
    def get_session(self):
        """
        Return a SessionBase instance or its subclass, if a 
        valid session is found.
        """
        this_session = NoTimeoutSessionManager.get_session(self)
        
        if self.is_session_timedout(this_session):
            self.expire_session()
            this_session = NoTimeoutSessionManager.get_session(self)
            #raise SessionError("The session has timed out.", result.id)
        
        this_session._slidingtimeout_access_time = this_session.get_access_time()

        return this_session
    


class FixedTimeoutSessionManager(NoTimeoutSessionManager):
    """
    Provides a fixed timeout capability.  What this means is 
    that the session will timeout after a certain amount of 
    time since first login.
    """    
   
    timeout_in_min = 1440 # 24 hours.


    def is_session_timedout(self, session_obj):
        """
        Return True if session has timed out, False otherwise.

        session_obj -- an instance of SessionBase or its subclass.
        """
        if session_obj.get_creation_age() >= self.timeout_in_min * 60:
            return True
        else:
            return False


    def get_session(self):
        """
        Return a SessionBase instance or its subclass, if a 
        valid session is found.
        """
        this_session = NoTimeoutSessionManager.get_session(self)
        
        if self.is_session_timedout(this_session):
            self.expire_session()
            this_session = NoTimeoutSessionManager.get_session(self)
            #raise SessionError("The session has timed out.", result.id)

        return this_session



def remove_dead_session(session_manager):
    """
    Deletes expired sessions.  This should be run by
    either a separate daemon program, or periodically
    by a thread.  See the SessionReaper class for a 
    prepackaged solution.

    session_manager -- an instance of a session manager
                       (Quixote.session.SessionManager) 
                       or its subclasses.
    """
    for session_id, session_obj in session_manager.items():
        if session_manager.is_session_timeout(session_obj):
            try:
                del session_manager[session_id]
            except KeyError:
                # May be the session has been deleted in 
                # the mean time, so just ignore the
                # error.
                pass



class SessionReaper(_threading.Thread):
    """
    A background thread class that can be used to
    clean up expired sessions, to avoid the session database
    getting too large.  

    A background (daemon) thread means that this thread
    will be killed once the main thread exits.
    
    Use like this:
    SessionReaper(60, session_manager).start()
    """
    def __init__(self, cleanup_in_min, session_manager):
        _threading.Thread.__init__(self)
        self._cleanup_in_min = cleanup_in_min
        self._session_manager = session_manager
        self.setName("SessionReaper thread created at: %s" % time())
        self.setDaemon(True)


    def run(self):
        while True:
            sleep(self._cleanup_in_min * 60)
            remove_dead_session(self._session_manager)

