import json
import http.cookies

from .response_headers import HttpResponseHeaders
from .status_codes import HttpStatusCodes
from .utils import dict2


class Response(object):
    __slots__ = ['_content', '_content_length', '_cookies',
                 '_headers', '_status_code']

    def __init__(self):
        self._content = 'None'
        self._content_length = None
        self._cookies = http.cookies.BaseCookie()
        self._headers = {HttpResponseHeaders.CONTENT_TYPE: 'text/html'}
        self._status_code = HttpStatusCodes.HTTP_200

    def set_status(self, status_code):
        self._status_code = status_code

    def set_header(self, key, value):
        self._headers[key] = value

    def set_cookie(self, key, value, domain=None, path='/', secure=None,
                   httponly=True):
        self._cookies[key] = value
        if domain:
            self._cookies[key]['domain'] = domain
        if path:
            self._cookies[key]['path'] = path
        if secure:
            self._cookies[key]['secure'] = secure
        if httponly:
            self._cookies[key]['httponly'] = httponly

    def set_content(self, content, content_length=None):
        if content_length:
            self._content_length = content_length
        self._content = content

    def bake(self, start_response):
        if isinstance(self._content, str):
            self._content = bytes(self._content, 'utf8')

        if self._content_length is None:
            self._content_length = len(self._content)

        self._headers[HttpResponseHeaders.CONTENT_LENGTH] = \
            str(self._content_length)
        headers = list(self._headers.items())
        cookies = [(HttpResponseHeaders.SET_COOKIE, v.OutputString())
                   for _, v in self._cookies.items()]

        if len(cookies):
            headers = list(headers) + cookies
        start_response(self._status_code, headers)

        if isinstance(self._content, bytes):
            return [self._content]

        return self._content

    # Helper functions
    def set_redirect(self, url, status=HttpStatusCodes.HTTP_303):
        self.set_status(status)
        self.set_content('')
        self.set_header(HttpResponseHeaders.LOCATION, url)

    def set_json(self, obj, status=HttpStatusCodes.HTTP_200):
        obj = json.dumps(obj, sort_keys=True, default=lambda x: str(x))
        self.set_status(status)
        self.set_header(HttpResponseHeaders.CONTENT_TYPE, 'application/json')
        self.set_content(obj)
