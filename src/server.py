import io
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler


class ServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print('Выполнен GET-запрос.')
        file = io.BytesIO()
        file.write('Вот он, первый GET-запрос.'.encode(encoding='utf-8'))
        file.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.copyfile(file, self.wfile)


class Server:
    def __init__(self, address: str, port: int):
        self.server_address = (address, port)
        self.server_class = HTTPServer
        self.handler_class = ServerHandler
        self.httpd = self.server_class(self.server_address, self.handler_class)

    def run(self):
        print(f'Запуск сервера по адресу {self.httpd.server_address[0]}:{self.httpd.server_address[1]}')
        self.httpd.serve_forever()
