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
            except Exception as e:
                self.ctx.response.set_json({
                    'status': 'ERROR',
                    'payload': 'Internal error.'
                })
        else:
            self.ctx.response.set_json({
                'status': 'ERROR',
                'errors': self.errors
            })

    def init(self):
        pass

    def validate(self):
        pass


class ViewEndpoint(Endpoint):
    def __call__(self):
        return self.call()
