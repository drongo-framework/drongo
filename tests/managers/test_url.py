from drongo.managers import UrlManager

import unittest


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

        self.manager.add(pattern='/', method='GET', call=a)
        self.manager.add(pattern='/test', call=b)
        self.manager.add(pattern='/hello', method=['GET', 'POST'], call=c)

        self.assertIs(a, self.manager.find_call('/', 'GET')[0])
        self.assertIs(b, self.manager.find_call('/test', 'GET')[0])
        self.assertIs(b, self.manager.find_call('/test/', 'GET')[0])
        self.assertIs(c, self.manager.find_call('/hello/', 'POST')[0])

    def test_params(self):
        def a():
            pass

        self.manager.add(pattern='/test/{param}', method='GET', call=a)
        _, params = self.manager.find_call('/test/hello', 'GET')

        self.assertEqual(params, [('param', 'hello')])
