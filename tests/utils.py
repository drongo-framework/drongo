from unittest import TestCase
from wsgiref.simple_server import make_server

from drongo import Drongo
from threading import Thread


class DrongoTestCase(TestCase):
    @classmethod
    def setUpClass(self):
        self.app = Drongo()
        self.httpd = make_server('', 5555, self.app)
        self.thread = Thread(target=self.httpd.serve_forever)
        self.thread.start()

    @classmethod
    def tearDownClass(self):
        self.httpd.server_close()
        self.httpd.shutdown()
