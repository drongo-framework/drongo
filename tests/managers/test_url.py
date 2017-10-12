import unittest

from drongo.managers import UrlManager


class TestUrlManager(unittest.TestCase):
    def setUp(self):
        self.manager = UrlManager()

    def test_basic(self):
        def a():
            pass

        def b():
            pass

        def c():
            pass

        def d():
            pass

        self.manager.add(pattern='/', method='GET', call=a)
        self.manager.add(pattern='/test', call=b)
        self.manager.add(pattern='/hello', method=['GET', 'POST'], call=c)
        self.manager.add(pattern='/world/*', method='GET', call=d)

        self.assertIs(a, self.manager.find_call('/', 'GET')[0])
        self.assertIs(b, self.manager.find_call('/test', 'GET')[0])
        self.assertIs(b, self.manager.find_call('/test/', 'GET')[0])
        self.assertIs(c, self.manager.find_call('/hello/', 'POST')[0])
        self.assertIs(d, self.manager.find_call('/world/a/b/c', 'GET')[0])
        self.assertIsNone(self.manager.find_call('/hello/world', 'POST'))
        self.assertIsNone(self.manager.find_call('/hello', 'PUT'))

    def test_params(self):
        def a():
            pass

        self.manager.add(pattern='/test/{param}', method='GET', call=a)
        self.manager.add(pattern='/test/{param}/test/*', method='GET', call=a)

        _, params = self.manager.find_call('/test/hello', 'GET')
        self.assertEqual(params, [('param', 'hello')])
        _, params = self.manager.find_call('/test/hello/test/world', 'GET')
        self.assertEqual(params, [('param', 'hello')])

    def test_named_url(self):
        def a():
            pass

        self.manager.add(pattern='/test', method='GET', call=a, name='test')
        self.assertEqual('/test/', self.manager.find_pattern('test'))
