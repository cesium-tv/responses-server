import logging
from unittest import TestCase

import requests
from responses import matchers
from responses_server import ResponsesServer


LOGGER = logging.getLogger()
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.ERROR)


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
        self.server.add('GET', self.server.url('/foobar'), status=200)
        r = requests.get(self.server.url('/foobar'))
        self.assertEqual(200, r.status_code)

    def test_querystring(self):
        self.server.get(self.server.url('/foobar', {'foo': 'bar'}), status=200)
        r = requests.get(self.server.url('/foobar'), params={'foo': 'bar'})
        self.assertEqual(200, r.status_code)

    def test_post(self):
        self.server.post(self.server.url(), match=[matchers.urlencoded_params_matcher({"left": "1", "right": "3"})])
        r = requests.post(self.server.url(), data={"left": 1, "right": 3})
        self.assertEqual(200, r.status_code)
