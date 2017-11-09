import json

try:
    from Cookie import BaseCookie
except ImportError:
    from http.cookies import BaseCookie

from .utils import dict2


__all__ = ['Request']


class Request(object):
    """Request class."""

    __slots__ = ['_env', '_query', '_cookies']

    def __init__(self, env):
        """Create request object from env."""
        self._env = env

        self._env['REQUEST_METHOD'] = self._env['REQUEST_METHOD'].upper()

        # Load the query params and form params
        self._query = {}
        self._query.update(env.get('GET'))
        self._query.update(env.get('POST', {}))

        # Load the cookies
        self._cookies = dict2()
        for cookie in BaseCookie(env.get('HTTP_COOKIE')).values():
            self._cookies[cookie.key] = cookie.value

    @property
    def cookies(self):
        """:obj:`drongo.utils.dict2` Dictionary of cookies."""
        return self._cookies

    @property
    def env(self):
        """:obj:`dict` Dictionary containing information about the request."""
        return self._env

    @property
    def method(self):
        """:obj:`str` HTTP method of the request."""
        return self._env['REQUEST_METHOD']

    @property
    def path(self):
        """:obj:`str` Resource path of the request."""
        return self._env['PATH_INFO']

    @property
    def query(self):
        """:obj:`drongo.utils.dict2` Dictionary of the GET and POST.

        Dictionary of the GET and POST (as applicable) query combined. Key
        represents the name in the form and each value is a :obj:`list` of
        corresponding values.
        """
        return self._query

    @property
    def json(self):
        """Request body loaded as json."""
        return json.loads(self.env['BODY'].decode('utf-8'))
