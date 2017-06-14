from .request import Request
from .response import Response
from .status_codes import HttpStatusCodes
from .utils import dict2

import logging
import sys
import traceback


class UrlManager(object):
    def __init__(self):
        self._routes = {}

    def add_url(self, pattern, method=None, call=None):
        if not pattern.endswith('/'):
            pattern += '/'
        parts = tuple(pattern.split('/')[1:])
        node = self._routes
        for part in parts:
            node = node.setdefault(part, {})
        if method is None:
            node['GET'] = call
        elif isinstance(method, str):
            node[method] = call
        else:
            for m in method:
                node[m] = call

    def find_call(self, path, method):
        if not path.endswith('/'):
            path += '/'
        path = path.split('/')[1:]
        return self._recursive_route_match(self._routes, path, method, [])

    def _recursive_route_match(self, node, remaining, method, args):
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
                result = self._recursive_route_match(node[key], remaining[1:],
                                                     method, args)
                if result:
                    return result
            elif len(key) and key[0] == '{':
                # We match for concrete part first and then compare
                # parameterised parts.
                continue
        for key in node:
            if len(key) and key[0] == '{':
                result = self._recursive_route_match(
                    node[key], remaining[1:], method,
                    args + [(key[1:-1], remaining[0])]
                )
                if result:
                    return result
        return None


class Drongo(object):
    def __init__(self):
        self.context = dict2()
        self._url_manager = UrlManager()
        self._middlewares = []
        self._logger = logging.getLogger('drongo')

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
        match = self._url_manager.find_call(request.path, request.method)

        if match:
            meth, args = match
            ctx.callable = meth
            ctx.callable_args = args

            # Convert tuple to dictionary
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

                for mw in self._middlewares:
                    if hasattr(mw, 'exception'):
                        mw.exception(ctx)
                exc_type, exc_value, exc_traceback = sys.exc_info()

                self._logger.error('\n'.join(traceback.format_exception(
                    exc_type, exc_value, exc_traceback)))

        else:
            response.set_status(HttpStatusCodes.HTTP_404)
            response.set_content('Not found!')

        # Returns empty response in case of no match
        self._logger.info('{method}\t{path}\t{status}'.format(
            method=request.method, path=request.path,
            status=response._status_code))
        return response.bake(start_response)

    def url(self, pattern, method=None):
        def _inner(call):
            self._url_manager.add_url(pattern, method, call)
            return call
        return _inner

    def add_url(self, pattern, method=None, call=None):
        self._url_manager.add_url(pattern, method, call)
