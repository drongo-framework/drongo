import unittest

from drongo.request import Request


class TestRequest(unittest.TestCase):
    def test_request(self):
        env = dict(
            REQUEST_METHOD='GET',
            GET=dict(hello='world'),
            PATH_INFO='/home',
            HTTP_COOKIE='a=b'
        )
        req = Request(env)
        self.assertEqual(req.method, 'GET')
        self.assertEqual(req.path, '/home')
        self.assertEqual(req.query, dict(hello='world'))
        self.assertEqual(req.cookies['a'], 'b')
        self.assertEqual(env, req.env)

    def test_json(self):
        env = dict(
            REQUEST_METHOD='POST',
            GET={},
            PATH_INFO='/home',
            BODY=b'{"hello": "world"}'
        )
        req = Request(env)
        self.assertEqual(dict(hello='world'), req.json)
