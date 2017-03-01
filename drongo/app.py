from .request import Request
from .response import Response, CustomResponse
from .status_codes import HTTP_STATUS_CODES


class Application(object):
    def __init__(self):
        self.routes = {}
        self.middlewares = []

    def __call__(self, env, start_response):
        request = Request(env)
        skip_request = False

        for middleware in self.middlewares:
            response = middleware.pre_request(request)
            if response is not None:
                skip_request = True
                break

        if not skip_request:
            match = self.match_route(request.path)
            if match:
                meth, args = match
                args = {k: v for k, v in args}
                response = meth(request, **args)
            else:
                response = CustomResponse(HTTP_STATUS_CODES[404], 'text/plain',
                                          b'Not Found!')

        for middleware in self.middlewares[::-1]:
            new_response = middleware.post_request(request, response)
            if new_response is not None:
                response = new_response
                break

        if isinstance(response, str):
            response = Response(response)
        elif isinstance(response, tuple):
            status, content_type, body = response
            response = CustomResponse(status, content_type, body)
        return response.bake(start_response)

    def route(self, urlpattern):
        if not urlpattern.endswith('/'):
            urlpattern += '/'
        parts = tuple(urlpattern.split('/')[1:])

        def _inner(method):
            method.__url__ = urlpattern
            node = self.routes
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node[parts[-1]] = method

            return method
        return _inner

    def recursive_route_match(self, node, remaining, args):
        if len(remaining) == 0:
            if callable(node):
                return (node, args)
            else:
                return None

        result = None
        for key in node:
            if key == remaining[0]:
                result = self.recursive_route_match(node[key], remaining[1:],
                                                    args)
                if result:
                    return result
            elif len(key) and key[0] == '{':
                continue
        for key in node:
            if len(key) and key[0] == '{':
                result = self.recursive_route_match(
                    node[key], remaining[1:],
                    args + [(key[1:-1], remaining[0])]
                )
                if result:
                    return result
        return None

    def match_route(self, path):
        if not path.endswith('/'):
            path += '/'
        path = path.split('/')[1:]
        return self.recursive_route_match(self.routes, path, [])
