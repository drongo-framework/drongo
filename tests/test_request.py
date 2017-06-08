from drongo.request import Request

import unittest


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
