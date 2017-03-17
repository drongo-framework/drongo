import json
import http.cookies

from .response_headers import HttpResponseHeaders
from .status_codes import HttpStatusCodes
from .utils import dict2


class Response(object):
    __slots__ = ['_content', '_content_length', '_context', '_cookies',
                 '_headers', '_status_code']

    def __init__(self):
        self._content = 'None'
        self._content_length = None
        self._context = dict2()
        self._cookies = http.cookies.BaseCookie()
        self._headers = {HttpResponseHeaders.CONTENT_TYPE: 'text/html'}
        self._status_code = HttpStatusCodes.HTTP_200

    context = property(lambda self: self._context)

    def set_status(self, status_code):
        self._status_code = status_code

    def set_header(self, key, value):
        self._headers[key] = value

    def set_cookie(self, key, value):
        self._cookies[key] = value

    def set_content(self, content, content_length=None):
        self._content_length = content_length
        self._content = content

    def bake(self, start_response):
        if isinstance(self._content, str):
            self._content = bytes(self._content, 'utf8')

        if self._content_length is None:
            self._content_length = len(self._content)

        self._headers[HttpResponseHeaders.CONTENT_LENGTH] = \
            str(len(self._content))
        headers = list(self._headers.items())
        cookies = [(HttpResponseHeaders.SET_COOKIE, v.OutputString())
                   for _, v in self._cookies.items()]

        if len(cookies):
            headers = list(headers) + cookies
        start_response(self._status_code, headers)

        if isinstance(self._content, bytes):
            return [self._content]

        return self._content
