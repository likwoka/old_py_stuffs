# TODO ... Unfinished!!!

class Cache:
    
    def __init__(self, store={}, max_size=None):
        self._store = store
        self.max_size = max_size


    def get(self, key):
        pass


    def set(self, cache_entry):
        pass


    def has_key(self, key):
        pass


    def __len__(self):
        pass


class NoTimeoutCacheEntry:
    def __init__(self, key, value)


class FixedTimeoutCacheEntry:
    def __init__(self, key, value, timeout_sec=):
        pass


class SlidingTimeoutCacheEntry:
    def __ini__(self, key, value, timeout_sec=):
        pass


class CacheKey:
    def __init__(*args):
        pass


