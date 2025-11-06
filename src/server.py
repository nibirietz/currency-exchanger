from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

from src.dto.currency_post_dto import CurrencyPost
from src.router import Router
from src.service import Service

router = Router()


class ServerHandler(BaseHTTPRequestHandler):
    service = Service()

    def _find_route(self, method: str, path: str):
        if (method, path) in router.routes:
            return router.routes[(method, path)], {}

        for pattern_route in router.pattern_routes:
            if pattern_route["method"] == method:
                result = pattern_route["parser"].parse(path)
                if result:
                    return pattern_route["function"], result.named

        return self.not_founded(), {}

    def _request_parse_request(self):
        parsed_path = urlparse(self.path)
        query_parameters = parse_qs(parsed_path.query)

        simple_query_params = {}

        for key, item in query_parameters.items():
            if len(item) == 1:
                simple_query_params[key] = item[0]
            else:
                simple_query_params[key] = item

        return {
            'path': parsed_path.path,
            'query_parameters': simple_query_params,
        }

    def _handle_method(self, method: str):
        request_data = self._request_parse_request()
        handler, path_parameters = self._find_route(method, request_data['path'])
        if (method, request_data['path']) not in router.routes.keys():
            self.not_founded()
            return
        # handler = router.routes[(method, request_data['path'])]
        # print(handler, path_parameters)
        if len(request_data['query_parameters']) != 0:
            handler(self, **path_parameters, **request_data['query_parameters'])
        else:
            handler(self, **path_parameters)

    def parse_body_to_dict(self) -> dict:
        content_length = int(self.headers['Content-Length'])
        raw_body = self.rfile.read(content_length)
        raw_dict = parse_qs(raw_body)
        result = {key.decode(): value[0].decode() for key, value in raw_dict.items()}
        for key, value in result.items():
            if value.isdigit():
                result[key] = float(value) if float(value) != int(value) else int(value)

        print(result)
        return result

    def not_founded(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Not founded.'.encode())

    def do_GET(self):
        self._handle_method('GET')
        print(self.path)

    def do_POST(self):
        self._handle_method('POST')
        print(self.path)

    @router.route(method='GET', path='/')
    def get_root(self):
        try:
            self.send_response(202)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps('Hello!').encode())
        except NotImplemented:
            self.send_response(400)
            self.wfile.write(json.dumps('Not Implemented').encode())

    @router.route(method='GET', path='/currencies')
    def get_currencies(self):
        self.send_response(202)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        currencies = self.service.get_currencies()
        self.wfile.write(json.dumps(currencies).encode())

    @router.route(method='GET', path='/currency/{currency_name}')
    def get_currency(self, currency_name: str):
        self.send_response(202)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        currency = self.service.get_currency(currency_name)
        self.wfile.write(json.dumps(currency).encode())

    @router.route(method='POST', path='/currencies')
    def add_currency(self):
        try:
            currency_post = CurrencyPost(**self.parse_body_to_dict())
            self.service.post_currency(currency_post)
        except TypeError:
            self.send_error(400)
        self.send_response(202)
        self.end_headers()
