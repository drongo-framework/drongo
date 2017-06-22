from .managers import MiddlewareManager, UrlManager
from .request import Request
from .response import Response
from .status_codes import HttpStatusCodes
from .utils import dict2

import logging
import sys
import traceback


class Drongo(object):
    def __init__(self):
        self.context = dict2()
        self._url_manager = UrlManager()
        self._mw_manager = MiddlewareManager()
        self._logger = logging.getLogger('drongo')

    def add_middleware(self, middleware):
        self._mw_manager.add(middleware)

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
                self._mw_manager.call_before(ctx)

                ret = meth(ctx, **args)
                if ret is not None:
                    # TODO: Check for types if really necessary!
                    response.set_content(ret)

                self._mw_manager.call_after(ctx)

            except Exception as e:
                response.set_status(HttpStatusCodes.HTTP_500)
                response.set_content('Internal server error!')

                self._mw_manager.call_exception(ctx, e)
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

    # Properties
    @property
    def urls(self):
        return self._url_manager

    @property
    def middlewares(self):
        return self._mw_manager
