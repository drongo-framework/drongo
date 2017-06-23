import json
import six

try:
    from Cookie import BaseCookie
except ImportError:
    from http.cookies import BaseCookie

from .response_headers import HttpResponseHeaders
from .status_codes import HttpStatusCodes
from .utils import dict2


class Response(object):
    __slots__ = ['_content', '_content_length', '_cookies',
                 '_headers', '_status_code']

    def __init__(self):
        self._content = 'None'
        self._content_length = None
        self._cookies = BaseCookie()
        self._headers = {HttpResponseHeaders.CONTENT_TYPE: 'text/html'}
        self._status_code = HttpStatusCodes.HTTP_200

    def set_status(self, status_code):
        """Set status code for the response.

        Args:
            status_code (:obj:`str`): HTTP status

        See Also:
            :class:`drongo.status_codes.HttpStatusCodes`
        """
        self._status_code = status_code

    def set_header(self, key, value):
        """Set a response header.

        Args:
            key (:obj:`str`): Header name
            value (:obj:`str`): Header value

        See Also:
            :class:`drongo.response_headers.HttpResponseHeaders`
        """
        self._headers[key] = value

    def set_cookie(self, key, value, domain=None, path='/', secure=False,
                   httponly=True):
        """Set a cookie.

        Args:
            key (:obj:`str`): Cookie name
            value (:obj:`str`): Cookie value
            domain (:obj:`str`): Cookie domain
            path (:obj:`str`): Cookie value
            secure (:obj:`bool`): True if secure, False otherwise
            httponly (:obj:`bool`): True if it's a HTTP only cookie, False
                otherwise
        """
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
        """Set content for the response.

        Args:
            content (:obj:`str` or :obj:`iterable`): Response content. Can be
                either unicode or raw bytes. When returning large content,
                an iterable (or a generator) can be used to avoid loading
                entire content into the memory.
            content_length (:obj:`int`, optional): Content length. Length will
                be determined if not set. If content is an iterable, it's a
                good practise to set the content length.
        """
        if content_length is not None:
            self._content_length = content_length
        self._content = content

    def bake(self, start_response):
        """Bakes the response and returns the content.

        Args:
            start_response (:obj:`callable`): Callback method that accepts
                status code and a list of tuples (pairs) containing headers'
                key and value respectively.
        """
        if isinstance(self._content, six.text_type):
            self._content = self._content.encode('utf8')

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

        if isinstance(self._content, six.binary_type):
            return [self._content]

        return self._content

    # Helper functions
    def set_redirect(self, url, status=HttpStatusCodes.HTTP_303):
        """Helper method to set a redirect response.

        Args:
            url (:obj:`str`): URL to redirect to
            status (:obj:`str`, optional): Status code of the response
        """
        self.set_status(status)
        self.set_content('')
        self.set_header(HttpResponseHeaders.LOCATION, url)

    def set_json(self, obj, status=HttpStatusCodes.HTTP_200):
        """Helper method to set a JSON response.

        Args:
            obj (:obj:`object`): JSON serializable object
            status (:obj:`str`, optional): Status code of the response
        """
        obj = json.dumps(obj, sort_keys=True, default=lambda x: str(x))
        self.set_status(status)
        self.set_header(HttpResponseHeaders.CONTENT_TYPE, 'application/json')
        self.set_content(obj)
