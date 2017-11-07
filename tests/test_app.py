import unittest


from drongo import Drongo
from drongo.exceptions import SkipExecException


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = Drongo()

    def test_basic(self):
        def start_response(status_code, headers):
            pass

        @self.app.url('/home')
        def home(ctx):
            return ctx.request.query.get('hello')[0]

        def error(ctx):
            raise Exception('Testing error')

        self.app.add_url(pattern='/error', call=error)

        env = dict(
            REQUEST_METHOD='GET',
            GET=dict(hello=['world']),
            PATH_INFO='/home',
            HTTP_COOKIE='a=b'
        )
        result = list(self.app(env, start_response))
        self.assertEqual(b'world', b''.join(result))

        env['PATH_INFO'] = '/hello'
        result = list(self.app(env, start_response))
        self.assertEqual(b'Not found!', b''.join(result))

        env['PATH_INFO'] = '/error'
        result = list(self.app(env, start_response))
        self.assertEqual(b'Internal server error!', b''.join(result))

    def test_middleware(self):
        def start_response(status_code, headers):
            pass

        class MyMiddleware(object):
            def before(self, ctx):
                pass

            def after(self, ctx):
                pass

            def exception(self, ctx, exc):
                pass

        self.app.add_middleware(MyMiddleware())

        @self.app.url('/home')
        def home(ctx):
            return ctx.request.query.get('hello')[0]

        def error(ctx):
            raise Exception('Testing error')

        self.app.urls.add(pattern='/error', call=error)

        env = dict(
            REQUEST_METHOD='GET',
            GET=dict(hello=['world']),
            PATH_INFO='/home',
            HTTP_COOKIE='a=b'
        )
        result = list(self.app(env, start_response))
        self.assertEqual(b'world', b''.join(result))

        env['PATH_INFO'] = '/error'
        result = list(self.app(env, start_response))
        self.assertEqual(b'Internal server error!', b''.join(result))

    def test_middleware_override_exec(self):
        def start_response(status_code, headers):
            pass

        class MyMiddleware(object):
            def before(self, ctx):
                ctx.response.set_content(b'skipworld')
                raise SkipExecException

            def after(self, ctx):
                pass

            def exception(self, ctx, exc):
                pass

        self.app.middlewares.add(MyMiddleware())

        @self.app.url('/home')
        def home(ctx):
            return ctx.request.query.get('hello')[0]

        env = dict(
            REQUEST_METHOD='GET',
            GET=dict(hello=['world']),
            PATH_INFO='/home',
            HTTP_COOKIE='a=b'
        )
        result = list(self.app(env, start_response))
        self.assertEqual(b'skipworld', b''.join(result))
