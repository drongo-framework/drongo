class MiddlewareManager(object):
    def __init__(self):
        self._middlewares = []

    def add(self, middleware):
        self._middlewares.append(middleware)

    def call_before(self, ctx):
        for mw in self._middlewares:
            if hasattr(mw, 'before'):
                mw.before(ctx)

    def call_after(self, ctx):
        for mw in self._middlewares[::-1]:
            if hasattr(mw, 'after'):
                mw.after(ctx)

    def call_exception(self, ctx, exc):
        for mw in self._middlewares:
            if hasattr(mw, 'exception'):
                mw.exception(ctx)
