from drongo.middleware import Middleware
from drongo.response import Redirect


class AddSlashMiddleware(Middleware):
    def pre_request(self, request):
        if not request.path.endswith('/'):
            return Redirect(request.path + '/')
