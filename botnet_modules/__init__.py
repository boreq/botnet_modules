import datetime
import hashlib
import requests


_uagent = 'Mozilla/5.0 (X11; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'


def get_url(*args, **kwargs):
    method = kwargs.pop('method', None)
    if method is None:
        method = 'get'
    method = method.upper()

    if not 'headers' in kwargs:
        kwargs['headers'] = {}
    kwargs['headers']['User-Agent'] = _uagent

    return requests.request(method, *args, **kwargs)


def get_md5(string):
    """Returns a hash of a string."""
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


class MemoryCache(object):
    """Cache which can be used by modules, 100% thread unsafety guaranteed."""

    def __init__(self, default_timeout):
        self.default_timeout = default_timeout
        self._data = {}

    def _prepare_key(self, key):
        return get_md5(key)

    def _clean(self):
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
