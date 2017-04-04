try:
    import thread as _thread
except ImportError:
    import dummy_thread as _thread

from quixote.publish import Publisher


class ThreadedPublisher(Publisher):
    """
    This publisher can handle multiple request at one time.  Each
    request's info will be stored in the thread's local storage.
    This publisher is intended for used with a multi-threading
    process.
    
    One publisher per process.  One publisher per many request.  
    One thread per request.  
    """
    
    def __init__(self, root_directory, logger=None, session_manager=None,
                 config=None, **kwargs):
        Publisher.__init__(self, root_directory, logger, session_manager,
                           config, **kwargs)
        self._request_dict = {}
        del self._request
        

    def _set_request(self, request):
        self._request_dict[_thread.get_ident()] = request


    def _clear_request(self):
        try:
            del self._request_dict[_thread.get_ident()]
        except KeyError:
            pass


    def get_request(self):
        return self._request_dict.get(_thread.get_ident())


