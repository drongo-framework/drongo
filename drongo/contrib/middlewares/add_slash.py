from drongo.response import Redirect

from .base import Middleware


class AddSlashMiddleware(Middleware):
    def pre_request(self, request):
        if not request.path.endswith('/'):
            return Redirect(request.path + '/')
