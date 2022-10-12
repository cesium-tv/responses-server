import time
import logging
import threading
import http.client
from urllib.parse import urljoin
from http.server import BaseHTTPRequestHandler, HTTPServer as BaseHTTPServer

from requests import Request
from requests.exceptions import ConnectionError
from requests.adapters import HTTPAdapter
from responses import RequestsMock


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle_any(self):
        url = self.server._responses.url(self.path)
        adapter = HTTPAdapter()
        kwargs = {
            'headers': self.headers,
        }
        content_length = self.headers.get('Content-Length', 0)
        if content_length:
            kwargs['data'] = self.rfile.read(content_length)
        request = Request(self.command, url, **kwargs).prepare()

        try:
            response = self.server._responses.responses._on_request(adapter, request)

        except ConnectionError:
            LOGGER.debug('Non-matching request')
            self.send_response(404)
            self.end_headers()

        else:
            self.send_response(response.status_code)
            for name, value in response.headers.items():
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(response.content)

    # Handle all HTTP verbs using our universal handler.
    do_GET = do_POST = do_HEAD = do_PUT = handle_any


class HTTPServer(BaseHTTPServer):
    def __init__(self, addr, handler, server):
        self._responses = server
        super().__init__(addr, handler)


class ResponsesServer:
    def __init__(self, address='127.0.0.1', port=0):
        self._address = address
        self._port = port
        self._thread = None
        self._server = None
        self.responses = RequestsMock()

    @property
    def port(self):
        return self._server and self._server.server_address[1] or 0

    @property
    def address(self):
        return self._address

    def url(self, path=None):
        url = f'http://{self.address}:{self.port}/'
        if path:
            url = urljoin(url, path)
        return url

    def start(self, **kwargs):
        self._server = HTTPServer((self._address, self._port), HTTPRequestHandler, self)
        self._thread = threading.Thread(target=self._run, **kwargs)
        self._thread.start()
        LOGGER.info('Server running at: %s', self.url)

    def stop(self):
        if self._server is None:
            return
        self._server.shutdown()
        self._server = None
        LOGGER.info('Server stopped')

    def join(self):
        LOGGER.debug('Joining thread %i', threading.get_ident())
        self._thread.join()

    def _run(self):
        LOGGER.debug('Serving forever in thread %i', threading.get_ident())
        self._server.serve_forever()
