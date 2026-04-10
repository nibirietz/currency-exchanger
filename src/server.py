from dataclasses import asdict
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

from src.database.models import Currency
from src.dto.currency_post_dto import CurrencyPost
from src.router import Router
from src.service import Service, CurrencyAlreadyExistsError, CurrencyNotFoundError

router = Router()


def create_handler(injection_service: Service) -> BaseHTTPRequestHandler:
    class ServerHandler(BaseHTTPRequestHandler):
        service = injection_service

        def _find_route(self, method: str, path: str):
            if (method, path) in router.routes:
                return router.routes[(method, path)], {}

            for pattern_route in router.pattern_routes:
                if pattern_route["method"] == method:
                    result = pattern_route["parser"].parse(path)
                    if result:
                        return pattern_route["function"], result.named

            return None, {}

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
            if handler is None:
                self.not_founded()
                return

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
            self.send_json(404, {"error": "Страница не найдена."})

        def do_GET(self):
            self._handle_method('GET')
            print(self.path)

        def do_POST(self):
            self._handle_method('POST')
            print(self.path)

        @router.route(method='GET', path='/')
        def get_root(self):
            try:
                self.send_json(202, {"message": "Это главная страница."})
            except NotImplemented:
                self.send_response(400)
                self.wfile.write(json.dumps('Not Implemented').encode())

        @router.route(method='GET', path='/currencies')
        def get_currencies(self):
            currencies: list[Currency] = self.service.get_all_currencies()
            currencies_view: list[dict] = [asdict(currency) for currency in currencies]
            self.send_json(202, currencies_view)

        @router.route(method='GET', path='/currency/{currency_name}')
        def get_currency(self, currency_name: str):
            try:
                currency = self.service.get_currency(currency_name)
                currency_view = asdict(currency)
                self.send_json(202, currency_view)
            except CurrencyNotFoundError as e:
                self.send_json(404, {"error": e})

        @router.route(method='GET', path='/currency')
        def get_currency_missing_code(self):
            self.send_json(400, {"error": "Код валюты не написан в адресе."})

        @router.route(method='POST', path='/currencies')
        def add_currency(self):
            currency_view = self.parse_body_to_dict()
            try:
                currency_post = CurrencyPost(name=currency_view["name"], code=currency_view["code"],
                                             sign=currency_view["sign"])
                self.service.add_currency(currency_post)
            except ValueError as e:
                self.send_json(400, {"error": str(e)})
            except CurrencyAlreadyExistsError as e:
                self.send_json(409, {"error": str(e)})

            self.send_json(202, currency_view)

        def send_json(self, status: int, data: dict | list[dict]):
            response = json.dumps(data).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

    return ServerHandler
