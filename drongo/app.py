from .request import Request
from .response import Response
from .status_codes import HttpStatusCodes
from .utils import dict2


class Drongo(object):
    def __init__(self):
        self.routes = {}
        self.context = dict2()
        self._middlewares = []

    def add_middleware(self, middleware):
        self._middlewares.append(middleware)

    def __call__(self, env, start_response):
        ctx = dict2()
        ctx.update(self.context)
        # Create the request
        request = ctx.request = Request(env)

        # Create the response
        response = ctx.response = Response()

        # Route matching
        match = self.match_route(request.path, request.method)
        if match:
            meth, args = match
            args = {k: v for k, v in args}
            try:
                for mw in self._middlewares:
                    if hasattr(mw, 'before'):
                        mw.before(ctx)

                ret = meth(ctx, **args)
                if ret is not None:
                    # TODO: Check for types if really necessary!
                    response.set_content(ret)

                for mw in self._middlewares[::-1]:
                    if hasattr(mw, 'after'):
                        mw.after(ctx)

            except Exception as e:
                response.set_status(HttpStatusCodes.HTTP_500)
                response.set_content('Internal server error!')
                raise e
                for mw in self._middlewares:
                    if hasattr(mw, 'exception'):
                        mw.exception(ctx)

        else:
            response.set_status(HttpStatusCodes.HTTP_404)
            response.set_content('Not found!')
        # Returns empty response in case of no match

        return response.bake(start_response)

    def route(self, urlpattern, method=None):
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
