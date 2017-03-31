from .utils import DrongoTestCase
import requests


class TestGet(DrongoTestCase):
    def test_404(self):
        result = requests.get('http://localhost:5555/')
        self.assertEqual(result.status_code, 404)

    def test_simple(self):
        @self.app.route(urlpattern='/simple', method='GET')
        def hello(ctx):
            return 'hello'

        result = requests.get('http://localhost:5555/simple')
        self.assertEqual(result.text, 'hello')

    def test_query(self):
        @self.app.route(urlpattern='/query', method='GET')
        def hello(ctx):
            return ctx.request.query['name'][0]

        result = requests.get('http://localhost:5555/query', {'name': 'test'})
        self.assertEqual(result.text, 'test')

    def test_multi_query(self):
        @self.app.route(urlpattern='/multi/query', method='GET')
        def hello(ctx):
            return ','.join(ctx.request.query['name'])

        data = {'name': ['test1', 'test2']}
        result = requests.get('http://localhost:5555/multi/query', data)
        self.assertEqual(result.text, 'test1,test2')

    def test_param_match_1(self):
        @self.app.route(urlpattern='/param/match/1/{name}', method='GET')
        def hello(ctx, name):
            return name

        result = requests.get('http://localhost:5555/param/match/1/test')
        self.assertEqual(result.text, 'test')

    def test_param_match_2(self):
        @self.app.route(urlpattern='/params/{name1}/{name2}', method='GET')
        def hello(ctx, name1, name2):
            return name1 + name2

        result = requests.get('http://localhost:5555/params/hello/world')
        self.assertEqual(result.text, 'helloworld')

    def test_disallowed_method(self):
        @self.app.route(urlpattern='/hello/disallowed', method='GET')
        def hello(ctx):
            return 'hello'

        result = requests.post('http://localhost:5555/hello/disallowed')
        self.assertEqual(result.status_code, 404)

    def test_allowed_method(self):
        @self.app.route(urlpattern='/hello/allowed', method=['GET', 'POST'])
        def hello(ctx):
            return 'hello'

        result = requests.get('http://localhost:5555/hello/allowed')
        self.assertEqual(result.text, 'hello')
