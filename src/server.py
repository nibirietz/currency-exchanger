from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
import json
from parse import compile
from urllib.parse import urlparse, parse_qs

from src.service import Service

service = Service()


class Router:
    def __init__(self):
        self.routes = {}
        self.pattern_routes = []

    def route(self, method: str, path: str):
        def decorator(func):
            if '{' in path or '}' in path:
                parser = compile(path)
                self.pattern_routes.append(
                    {
                        "parser": parser,
                        "function": func,
                        "method": method,
                        "path": path,
                    }
                )

            self.routes[(method, path)] = func

            return func

        return decorator


router = Router()


class ServerHandler(BaseHTTPRequestHandler):
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
        # if (method, request_data['path']) not in router.routes.keys():
        #     self.not_founded()
        #     return
        # handler = router.routes[(method, request_data['path'])]
        if len(request_data['query_parameters']) != 0:
            handler(self, **path_parameters, **request_data['query_parameters'])
        else:
            handler(self, **path_parameters)

    def not_founded(self):
        self.wfile.write('Not founded.'.encode())

    def do_GET(self):
        self._handle_method('GET')
        print(self.path)

    @router.route(method='GET', path='/currencies/')
    def get_currencies(self):
        self.send_response(202)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write('{ "RU": 1 }'.encode())

    @router.route(method='GET', path='/currency/{currency_id}')
    def get_currency(self, currency_id: int):
        self.send_response(202)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(f'{{"tst": {currency_id}}}'.encode())
