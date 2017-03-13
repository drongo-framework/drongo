from .request import Request
from .response import Response
from .utils import dict2


class Drongo(object):
    def __init__(self):
        self.routes = {}
        self.context = dict2()

    def __call__(self, env, start_response):
        # Create the request
        request = Request(env)
        request.context.update(self.context)

        # Create the response
        response = Response()

        # Route matching
        match = self.match_route(request.path)
        if match:
            meth, args = match
            args = {k: v for k, v in args}
            ret = meth(request, response, **args)
            if ret is not None:
                # TODO: Check for types if really necessary!
                response.set_content(ret)
        # Returns empty response in case of no match

        return response.bake(start_response)

    def route(self, urlpattern):
        if not urlpattern.endswith('/'):
            urlpattern += '/'
        parts = tuple(urlpattern.split('/')[1:])

        def _inner(method):
            node = self.routes
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node[parts[-1]] = method

            return method
        return _inner

    def add_route(self, urlpattern, method):
        if not urlpattern.endswith('/'):
            urlpattern += '/'
        parts = tuple(urlpattern.split('/')[1:])
        node = self.routes
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = method

    def recursive_route_match(self, node, remaining, args):
        # Route is stored in tree form for quick matching compared to
        # traditional form of regular expression matching
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
                # We match for concrete part first and then compare
                # parameterised parts.
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
