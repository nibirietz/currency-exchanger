from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

from src.service import Service

service = Service()


class Router:
    def __init__(self):
        self.routes = {}

    def route(self, method: str, path: str):
        def wrapper(func):
            self.routes[(method, path)] = func
            return func

        return wrapper


router = Router()


class ServerHandler(BaseHTTPRequestHandler):
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

    def handle_method(self, method: str):
        request_data = self._request_parse_request()
        handler = router.routes[(method, request_data['path'])]
        if len(request_data['query_parameters']) != 0:
            handler(self, request_data['query_parameters'])
        else:
            handler(self)

    def do_GET(self):
        print(router.routes)
        self.handle_method('GET')

    @router.route(method='GET', path='/currencies')
    def get_currencies(self, **kwargs):
        self.wfile.write('{}'.encode())
