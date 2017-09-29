import logging
import sys
import traceback

from drongo.status_codes import HttpStatusCodes


class Endpoint(object):
    __url__ = '/'
    __http_methods__ = ['GET']

    def __init__(self, ctx, **kwargs):
        self.ctx = ctx
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.valid = True
        self.errors = {}

    @classmethod
    def do(cls, ctx, **kwargs):
        ep = cls(ctx, **kwargs)
        return ep()

    def call(self):
        raise NotImplementedError


class APIEndpoint(Endpoint):
    _logger = logging.getLogger('drongo.api')

    def __call__(self):
        self.valid = True
        self.init()
        self.validate()

        if self.valid:
            try:
                self.ctx.response.set_json({
                    'status': 'OK',
                    'payload': self.call()
                })
                return

            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()

                self._logger.error('\n'.join(traceback.format_exception(
                    exc_type, exc_value, exc_traceback)))

                self.error('Internal server error.')
                self.status(HttpStatusCodes.HTTP_500)

        self.ctx.response.set_json({
            'status': 'ERROR',
            'errors': self.errors
        })

    def error(self, group='_', message=''):
        self.errors.setdefault(group, []).append(message)

    def status(self, status=HttpStatusCodes.HTTP_200):
        self.ctx.response.set_status(status)

    def init(self):
        pass

    def validate(self):
        pass


class ViewEndpoint(Endpoint):
    def __call__(self):
        return self.call()
