import cgi
import http.cookies
import urllib.parse

from .multipart import Multipart
from .utils import dict2


class Request(object):

    __slots__ = ['env', '_query', '_cookies']

    def __init__(self, env):
        self.env = env

        self.env['REQUEST_METHOD'] = self.env['REQUEST_METHOD'].upper()

        # Load the query params and form params
        inp = env.get('wsgi.input')
        self._query = urllib.parse.parse_qs(env.setdefault('QUERY_STRING', ''))

        if self.method == 'POST':
            self.process_post()

        # Load the cookies
        self._cookies = dict2()
        for cookie in http.cookies.BaseCookie(env.get('HTTP_COOKIE')).values():
            self._cookies[cookie.key] = cookie.value

    def process_post(self):
        content_type = self.env['CONTENT_TYPE']
        content_length = int(self.env['CONTENT_LENGTH'])
        if content_type == 'application/x-www-form-urlencoded':
            input = self.env['wsgi.input']
            post_data = b''
            while len(post_data) < content_length:
                post_data += input.read(content_length - len(post_data))
            post_query = urllib.parse.parse_qs(post_data.decode('utf8'))
            self._query.update(post_query)
        elif content_type.startswith('multipart/form-data'):
            print(content_length)
            boundary = content_type.split('boundary=')[1].encode('ascii')
            mp = Multipart(boundary, content_length, self.env['wsgi.input'])
            self._query.update(mp.parse())

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
