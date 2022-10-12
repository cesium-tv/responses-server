import logging
from unittest import TestCase

import requests
from responses_server import ResponsesServer


LOGGER = logging.getLogger()
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)


class ServerTestCase(TestCase):
    def setUp(self):
        self.server = ResponsesServer()
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_start_stop(self):
        self.server.stop()

    def test_request(self):
        r = requests.get(self.server.url())
        self.assertEqual(404, r.status_code)

    def test_match(self):
        self.server.responses.add('GET', self.server.url('/foobar'), status=200)
        r = requests.get(self.server.url('/foobar'))
        self.assertEqual(200, r.status_code)
