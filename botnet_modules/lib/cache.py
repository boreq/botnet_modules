import datetime
from .helpers import get_md5


class MemoryCache(object):
    """Simple cache. 100% thread unsafety guaranteed.
    
    default_timeout: timeout used by the set method [seconds].
    """

    def __init__(self, default_timeout):
        self.default_timeout = default_timeout
        self._data = {}

    def _prepare_key(self, key):
        """Prepares a key before using it."""
        return get_md5(key)

    def _clean(self):
        """Removes expired values."""
        for key in self._data.copy().keys():
            try:
                expires, value = self._data[key]
                if expires < datetime.datetime.now():
                    self._data.pop(key)
            except KeyError:
                pass

    def set(self, key, value, timeout=None):
        """Set a value."""
        self._clean()
        key = self._prepare_key(key)
        if timeout is None:
            timeout = self.default_timeout
        expires = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self._data[key] = (expires, value)

    def get(self, key):
        """Get a value."""
        try:
            key = self._prepare_key(key)
            expires, value = self._data[key]
            if expires > datetime.datetime.now():
                return value
            else:
                return None
        except KeyError:
            return None
