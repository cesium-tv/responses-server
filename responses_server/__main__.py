import logging

from responses_server import ResponsesServer


LOGGER = logging.getLogger()
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)


def main():
    server = ResponsesServer()
    server.start()

    try:
        server.join()

    except KeyboardInterrupt:
        server.stop()


if __name__ == '__main__':
    main()
