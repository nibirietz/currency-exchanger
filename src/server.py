import json
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from src.dto.currency_dto import CurrencyResponse
from src.exceptions import (
    CurrencyAlreadyExistsError,
    CurrencyNotFoundError,
    ExchangeRateAlreadyExistsError,
    ExchangeRateNotFoundError,
)
from src.mappers.currency_mapper import CurrencyMapper
from src.mappers.exchange_rate_mapper import ExchangeRateMapper
from src.router import Router
from src.services.currency_service import CurrencyService
from src.services.exchange_rate_service import ExchangeRateService

router = Router()


def create_handler(
    injected_currency_service: CurrencyService,
    injected_exchange_rate_service: ExchangeRateService,
) -> BaseHTTPRequestHandler:
    class ServerHandler(BaseHTTPRequestHandler):
        currency_service = injected_currency_service
        exchange_rate_service = injected_exchange_rate_service

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
                "path": parsed_path.path,
                "query_parameters": simple_query_params,
            }

        def _handle_method(self, method: str):
            try:
                request_data = self._request_parse_request()
                handler, path_parameters = self._find_route(
                    method, request_data["path"]
                )
                if handler is None:
                    self.not_found()
                    return

                if len(request_data["query_parameters"]) != 0:
                    handler(self, **path_parameters, **request_data["query_parameters"])
                else:
                    handler(self, **path_parameters)
            except Exception as e:
                self.send_json(500, {"message": "Внутренняя ошибка сервера."})
                print(str(e))

        def parse_body_to_dict(self) -> dict:
            content_length = int(self.headers["Content-Length"])
            raw_body = self.rfile.read(content_length)
            raw_dict = parse_qs(raw_body)
            result = {
                key.decode(): value[0].decode() for key, value in raw_dict.items()
            }

            return result

        def not_found(self):
            self.send_json(404, {"error": "Страница не найдена."})

        def do_GET(self):
            self._handle_method("GET")
            print(self.path)

        def do_POST(self):
            self._handle_method("POST")
            print(self.path)

        def do_PATCH(self):
            self._handle_method("PATCH")
            print(self.path)

        def send_json(self, status: int, data: dict | list[dict]):
            response = json.dumps(data).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        @router.route(method="GET", path="/")
        def get_root(self):
            self.send_json(200, {"message": "Это главная страница."})

        @router.route(method="GET", path="/currencies")
        def get_currencies(self):
            currencies: list[CurrencyResponse] = (
                self.currency_service.get_all_currencies()
            )
            currencies_view: list[dict] = [asdict(currency) for currency in currencies]
            self.send_json(200, currencies_view)

        @router.route(method="GET", path="/currency/{currency_name}")
        def get_currency(self, currency_name: str):
            try:
                currency = self.currency_service.get_currency(currency_name)
                currency_view = asdict(currency)
                self.send_json(200, currency_view)
            except CurrencyNotFoundError as e:
                self.send_json(404, {"message": str(e)})

        @router.route(method="GET", path="/currency")
        def get_currency_missing_code(self):
            self.send_json(400, {"message": "Код валюты не написан в адресе."})

        @router.route(method="POST", path="/currencies")
        def add_currency(self):
            currency_view = self.parse_body_to_dict()

            try:
                currency_post = CurrencyMapper.dict_to_request(currency_view)
                currency_response = self.currency_service.add_currency(currency_post)
                self.send_json(201, CurrencyMapper.response_to_dict(currency_response))
            except ValueError as e:
                self.send_json(400, {"message": str(e)})
            except KeyError:
                self.send_json(400, {"message": "Отсутствует поле."})
            except CurrencyAlreadyExistsError as e:
                self.send_json(409, {"message": str(e)})

        @router.route(method="GET", path="/exchangeRates")
        def get_all_exchange_rates(self):
            exchange_rates = self.exchange_rate_service.get_all_exchange_rates()
            exchange_rates_view = [
                ExchangeRateMapper.response_to_view(exchange_rate)
                for exchange_rate in exchange_rates
            ]
            self.send_json(200, exchange_rates_view)

        @router.route(method="GET", path="/exchangeRate/{codes}")
        def get_exchange_rate(self, codes: str):
            if len(codes) != 6:
                self.send_json(404, {"message": "Обменный курс не найден."})
                return
            base_code, target_code = codes[:3], codes[3:]

            try:
                exchange_rate = self.exchange_rate_service.get_exchange_rate(
                    base_code, target_code
                )
                self.send_json(200, ExchangeRateMapper.response_to_view(exchange_rate))
            except ExchangeRateNotFoundError as e:
                self.send_json(404, {"message": str(e)})

        @router.route(method="POST", path="/exchangeRates")
        def add_exchange_rate(self):
            try:
                exchange_rate_request = ExchangeRateMapper.dict_to_request(
                    self.parse_body_to_dict()
                )
                exchange_rate_response = self.exchange_rate_service.add_exchange_rate(
                    exchange_rate_request.base_currency_code,
                    exchange_rate_request.target_currency_code,
                    exchange_rate_request.rate,
                )
                self.send_json(
                    201, ExchangeRateMapper.response_to_view(exchange_rate_response)
                )
            except KeyError:
                self.send_json(400, {"message": "Отсутствует нужное поле формы."})
            except ExchangeRateAlreadyExistsError as e:
                self.send_json(409, {"message": str(e)})
            except CurrencyNotFoundError as e:
                self.send_json(404, {"message": str(e)})

        @router.route(method="PATCH", path="/exchangeRate/{codes}")
        def patch_exchange_rate(self, codes: str):
            body_dict = self.parse_body_to_dict()
            if "rate" not in body_dict:
                self.send_json(400, {"message": "Отсутствует необходимое поле."})
                return
            if len(codes) != 6:
                self.send_json(404, {"message": "Обменный курс не найден."})
                return
            base_code, target_code = codes[:3], codes[3:]

            rate = body_dict["rate"]
            try:
                exchange_rate = self.exchange_rate_service.patch_exchange_rate(
                    base_code, target_code, rate
                )
                exchange_rate_view = ExchangeRateMapper.response_to_view(exchange_rate)
                self.send_json(200, exchange_rate_view)
            except ExchangeRateNotFoundError as e:
                self.send_json(404, {"message": str(e)})

    return ServerHandler  # basedpyright:ignore[invalid-return-type]
