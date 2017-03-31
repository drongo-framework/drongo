from .utils import DrongoTestCase
import requests


class TestGet(DrongoTestCase):
    def test_404(self):
        result = requests.get('http://localhost:5555/')
        self.assertEqual(result.status_code, 404)

    def test_simple(self):
        @self.app.route(urlpattern='/hello', method='GET')
        def hello(ctx):
            return 'hello'

        result = requests.get('http://localhost:5555/hello')
        self.assertEqual(result.text, 'hello')

    def test_query(self):
        @self.app.route(urlpattern='/hello', method='GET')
        def hello(ctx):
            return ctx.request.query['name'][0]

        result = requests.get('http://localhost:5555/hello', {'name': 'test'})
        self.assertEqual(result.text, 'test')

    def test_multi_query(self):
        @self.app.route(urlpattern='/hello', method='GET')
        def hello(ctx):
            return ','.join(ctx.request.query['name'])

        data = {'name': ['test1', 'test2']}
        result = requests.get('http://localhost:5555/hello', data)
        self.assertEqual(result.text, 'test1,test2')

    def test_param_match_1(self):
        @self.app.route(urlpattern='/hello/{name}', method='GET')
        def hello(ctx, name):
            self.assertEqual(name, 'test')
            return name

    def test_param_match_1(self):
        @self.app.route(urlpattern='/hello/{name1}/{name2}', method='GET')
        def hello(ctx, name1, name2):
            return name1 + name2

        result = requests.get('http://localhost:5555/hello/hello/world')
        self.assertEqual(result.text, 'helloworld')

    def test_disallowed_method(self):
        @self.app.route(urlpattern='/hello', method='GET')
        def hello(ctx):
            return 'hello'

        result = requests.post('http://localhost:5555/hello')
        self.assertEqual(result.status_code, 404)
