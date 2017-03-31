import cgi
import http.cookies
import urllib.parse

from .utils import dict2


class Request(object):

    __slots__ = ['env', '_query', '_cookies']

    def __init__(self, env):
        self.env = env

        self.env['REQUEST_METHOD'] = self.env['REQUEST_METHOD'].upper()

        # Load the query params and form params
        inp = env.get('wsgi.input')
        self._query = urllib.parse.parse_qs(env.setdefault('QUERY_STRING', ''))

        # Load the cookies
        self._cookies = dict2()
        for cookie in http.cookies.BaseCookie(env.get('HTTP_COOKIE')).values():
            self._cookies[cookie.key] = cookie.value

    def process_files(self):
        fs = cgi.FieldStorage(inp, environ=env)
        for k in fs:
            fld = fs[k]
            is_file = False
            try:
                it = iter(fld)
                for item in it:
                    if hasattr(item, 'filename') and item.filename:
                        is_file = True
            except TypeError:
                if hasattr(fld, 'filename') and fld.filename:
                    is_file = True
            if not is_file:
                fld = fs.getlist(k)
            self._query[k] = fld

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
