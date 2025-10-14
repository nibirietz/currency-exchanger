from http.server import HTTPServer, BaseHTTPRequestHandler


class Server:
    def __init__(self, address: str, port: int):
        self.server_address = (address, port)
        self.server_class = HTTPServer
        self.handler_class = BaseHTTPRequestHandler
        self.httpd = self.server_class(self.server_address, self.handler_class)

    def run(self):
        print(f'Запуск сервера по адресу {self.httpd.server_address[0]}:{self.httpd.server_address[1]}')
        self.httpd.serve_forever()
