from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json


from src.service import Service

service = Service()


class ServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print('Выполнен GET-запрос.')
        self.send_header('Content-type', 'application/json; charset=utf-8')
        path = self.path.split('/')
        match path[1]:
            case '/':
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'OK'}).encode())
            case 'currencies':
                self.get_currencies()
            case 'currency':
                self.get_currency(path[2])
            case _:
                self.send_response(HTTPStatus.NOT_FOUND)
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'Page is not found.'}).encode())

    def get_currencies(self):
        try:
            currencies = service.get_currencies()
        except NotImplemented:
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            raise NotImplemented
        self.send_response(HTTPStatus.ACCEPTED)
        self.wfile.write(json.dumps(currencies).encode())

    def get_currency(self, currency: str):
        try:
            currency = service.get_currency()
        except NotImplemented:
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            raise NotImplemented
        self.send_response(HTTPStatus.ACCEPTED)
        self.wfile.write(json.dumps(currency).encode())


class Server:
    def __init__(self, address: str, port: int):
        self.server_address = (address, port)
        self.server_class = HTTPServer
        self.handler_class = ServerHandler
        self.httpd = self.server_class(self.server_address, self.handler_class)

    def run(self):
        print(f'Запуск сервера на порту {self.server_address[1]}')
        self.httpd.serve_forever()
