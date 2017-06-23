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
        self._mw_manager = MiddlewareManager()
        self._url_manager = UrlManager()
        self._logger = logging.getLogger('drongo')

    def add_middleware(self, middleware):
        """Add a middleware.

        Args:
            middleware: Instance of a middleware class
        See Also:
            :class:`drongo.managers.middleware.MiddlewareManager`
        """
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
                self._mw_manager._call_before(ctx)

                ret = meth(ctx, **args)
                if ret is not None:
                    # TODO: Check for types if really necessary!
                    response.set_content(ret)

                self._mw_manager._call_after(ctx)

            except Exception as e:
                response.set_status(HttpStatusCodes.HTTP_500)
                response.set_content('Internal server error!')

                self._mw_manager._call_exception(ctx, e)
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
        """Decorator to map url pattern to the callable.

        Args:
            pattern (:obj:`str`): URL pattern to add. This is usually '/'
                separated path. Parts of the URL can be parameterised using
                curly braces.
                Examples: "/", "/path/to/resource", "/resoures/{param}"
            method (:obj:`str`, :obj:`list` of :obj:`str`, optional): HTTP
                methods for the path specied. By default, GET method is added.
                Value can be either a single method, by passing a string, or
                multiple methods, by passing a list of strings.

        Note:
            A trailing '/' is always assumed in the pattern.

        Example:
            >>> @app.url(pattern='/path/to/resource', method='GET')
            >>> def function(ctx):
            >>>     return 'Hello world'

        See Also:
            :func:`drongo.managers.url.UrlManager.add`
        """
        def _inner(call):
            self._url_manager.add(pattern, method, call)
            return call
        return _inner

    def add_url(self, pattern, method=None, call=None):
        """Add a url pattern.

        Args:
            pattern (:obj:`str`): URL pattern to add. This is usually '/'
                separated path. Parts of the URL can be parameterised using
                curly braces.
                Examples: "/", "/path/to/resource", "/resoures/{param}"
            method (:obj:`str`, :obj:`list` of :obj:`str`, optional): HTTP
                methods for the path specied. By default, GET method is added.
                Value can be either a single method, by passing a string, or
                multiple methods, by passing a list of strings.
            call (callable): Callable corresponding to the url pattern and the
                HTTP method specified.

        Note:
            A trailing '/' is always assumed in the pattern.

        See Also:
            :func:`drongo.managers.url.UrlManager.add`
        """
        self._url_manager.add(pattern, method, call)

    # Properties
    @property
    def middlewares(self):
        """:obj:`drongo.managers.middleware.MiddlewareManager` App's middleware
        manager.
        """
        return self._mw_manager

    @property
    def urls(self):
        """:obj:`drongo.managers.url.UrlManager` App's URL manager.
        """
        return self._url_manager
