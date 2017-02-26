from drongo.middleware import Middleware
from drongo.status_codes import HTTP_STATUS_CODES

import mimetypes
import os


class StaticMiddleware(Middleware):
    def __init__(self, url, static_dir):
        self.url = url
        self.static_dir = static_dir

    def pre_request(self, request):
        if not request.path.startswith(self.url):
            return
        path = request.path[len(self.url):]
        if path[0] == '/':
            path = path[1:]
        path = os.path.join(self.static_dir, path)
        if os.path.exists(path):
            with open(path, 'rb') as fd:
                content_type = mimetypes.guess_type(path)[0]
                return HTTP_STATUS_CODES[200], content_type, fd.read()
