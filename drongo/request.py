import cgi
import http.cookies


class Request(object):
    def __init__(self, env):
        self.env = env

        # Load the query params and form params
        env.setdefault('QUERY_STRING', '')
        inp = env.get('wsgi.input')
        self._query = {}
        fs = cgi.FieldStorage(inp, environ=env)
        for k in fs:
            fld = fs[k]
            if not hasattr(fld, 'filename') or fld.filename is None:
                fld = fs.getlist(k)
            self._query[k] = fld

        # Load the cookies
        self._cookies = dict()
        for cookie in http.cookies.BaseCookie(env.get('HTTP_COOKIE')).values():
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
