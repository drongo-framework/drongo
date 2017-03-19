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
        request.context.request = request

        # Create the response
        response = Response()

        # Route matching
        match = self.match_route(request.path, request.method)
        if match:
            meth, args = match
            args = {k: v for k, v in args}
            ret = meth(request, response, **args)
            if ret is not None:
                # TODO: Check for types if really necessary!
                response.set_content(ret)
        # Returns empty response in case of no match

        return response.bake(start_response)

    def route(self, urlpattern, method=None):
        if not urlpattern.endswith('/'):
            urlpattern += '/'
        parts = tuple(urlpattern.split('/')[1:])

        def _inner(call):
            self.add_route(urlpattern, call, method)
            return call
        return _inner

    def add_route(self, urlpattern, call, method=None):
        if not urlpattern.endswith('/'):
            urlpattern += '/'
        parts = tuple(urlpattern.split('/')[1:])
        node = self.routes
        for part in parts:
            node = node.setdefault(part, {})
        if method is None:
            node['GET'] = call
            node['POST'] = call
        elif isinstance(method, str):
            node[method] = call
        else:
            for m in method:
                node[m] = call

    def recursive_route_match(self, node, remaining, method, args):
        # Route is stored in tree form for quick matching compared to
        # traditional form of regular expression matching
        if len(remaining) == 0:
            if callable(node.get(method)):
                return (node.get(method), args)
            else:
                return None

        result = None
        for key in node:
            if key == remaining[0]:
                result = self.recursive_route_match(node[key], remaining[1:],
                                                    method, args)
                if result:
                    return result
            elif len(key) and key[0] == '{':
                # We match for concrete part first and then compare
                # parameterised parts.
                continue
        for key in node:
            if len(key) and key[0] == '{':
                result = self.recursive_route_match(
                    node[key], remaining[1:], method,
                    args + [(key[1:-1], remaining[0])]
                )
                if result:
                    return result
        return None

    def match_route(self, path, method):
        if not path.endswith('/'):
            path += '/'
        path = path.split('/')[1:]
        return self.recursive_route_match(self.routes, path, method, [])
