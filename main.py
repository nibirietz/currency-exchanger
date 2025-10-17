from http.server import HTTPServer

from src.server import ServerHandler
from src.service import Service


def main():
    server = HTTPServer(('0.0.0.0', 8080), ServerHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
