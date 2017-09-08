class MiddlewareManager(object):
    """Manages middlewares for the application.

    Middleware is a piece of code that run for every request. Middlewares
    have callbacks that run before the request, after the request and during an
    exception.

    Example:
        ::

            class ExampleMiddleware:
                def before(self, ctx):
                    pass  # Before the request

                def after(self, ctx):
                    pass  # After the request

                def exception(self, ctx, exc):
                    pass  # During an exception

    Note:
        Exception occuring in the callbacks will also result in the exception
        callback. No exceptions must be raised from the exception callback as
        they will not be handled by the framework.
    """
    def __init__(self):
        self._middlewares = []

    def add(self, middleware):
        """Add a middleware to the manager.

        Args:
            middleware: Instance of a middleware class
        """
        self._middlewares.append(middleware)

    def _call_before(self, ctx):
        for mw in self._middlewares:
            if hasattr(mw, 'before'):
                mw.before(ctx)

    def _call_after(self, ctx):
        for mw in self._middlewares[::-1]:
            if hasattr(mw, 'after'):
                mw.after(ctx)

    def _call_exception(self, ctx, exc):
        for mw in self._middlewares:
            if hasattr(mw, 'exception'):
                mw.exception(ctx, exc)
