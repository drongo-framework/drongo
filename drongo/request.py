import cgi

try:
    from Cookie import BaseCookie
except ImportError:
    from http.cookies import BaseCookie

from .utils import dict2


class Request(object):
    __slots__ = ['env', '_query', '_cookies']

    def __init__(self, env):
        self.env = env

        self.env['REQUEST_METHOD'] = self.env['REQUEST_METHOD'].upper()

        # Load the query params and form params
        self._query = {}
        self._query.update(env.get('GET'))
        self._query.update(env.get('POST', {}))

        # Load the cookies
        self._cookies = dict2()
        for cookie in BaseCookie(env.get('HTTP_COOKIE')).values():
            self._cookies[cookie.key] = cookie.value

    @property
    def method(self):
        return self.env['REQUEST_METHOD']

    @property
    def path(self):
        return self.env['PATH_INFO']

    @property
    def query(self):
        return self._query

    @property
    def cookies(self):
        return self._cookies
