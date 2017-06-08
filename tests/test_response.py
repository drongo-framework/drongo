from drongo.response import Response

import unittest


class TestResponse(unittest.TestCase):
    def test_response(self):
        resp = Response()

        def start_response(status, headers):
            pass  # TODO: Add more checks here

        resp.set_cookie('hello', 'world', domain='localhost', secure=True)
        resp.set_content('hello world!')

        res = resp.bake(start_response)
        self.assertEqual(b''.join(res), b'hello world!')

    def test_generated_response(self):
        resp = Response()

        def start_response(status, headers):
            pass

        def content():
            yield b'hello world!'

        resp.set_content(content(), 12)
        res = resp.bake(start_response)
        self.assertEqual(b''.join(list(res)), b'hello world!')

    def test_redirect(self):
        resp = Response()
        resp.set_redirect('/redirect')

    def test_json(self):
        resp = Response()
        resp.set_json({'hello': 'world'})
