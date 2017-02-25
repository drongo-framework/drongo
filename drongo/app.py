from .request import Request
from .response import Response


class Application(object):
    def __init__(self):
        self.routes = {}

    def __call__(self, env, start_response):
        request = Request(env)
        m = self.match_route(request.path)
        if m:
            meth, args = m
            args = {k: v for k, v in args}
            response = meth(request, **args)
            if isinstance(response, str):
                response = Response(response)
        else:
            response = Response('Not Found!')  # TODO: Generate 404
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
