import threading
from decimal import Decimal
from http.server import HTTPServer
from pathlib import Path
from typing import Generator

import pytest

from src.database.create_database import create_db
from src.database.currency_dao import CurrencyDAO
from src.database.exchange_rate_dao import ExchangeRateDAO
from src.server import create_handler
from src.services.currency_service import CurrencyService
from src.services.exchange_rate_service import ExchangeRateService


@pytest.fixture
def db_path(tmp_path: Path):
    return tmp_path / "test.sqlite"


class TestCurrencyDAO(CurrencyDAO):
    pass


class TestExchangeRateDAO(ExchangeRateDAO):
    def add_exchange_rate_by_id(self, base_id: int, target_id: int, rate: Decimal) -> int:
        query = """INSERT INTO exchange_rates (base_currency_id, target_currency_id, rate) VALUES (?, ?, ?);"""
        return self._execute_returning_last_row_id(query, (base_id, target_id, str(rate)))


@pytest.fixture
def currency_dao(db_path) -> TestCurrencyDAO:
    return TestCurrencyDAO(str(db_path))


@pytest.fixture
def exchange_rate_dao(db_path) -> TestExchangeRateDAO:
    return TestExchangeRateDAO(str(db_path))


@pytest.fixture
def server_url(db_path) -> Generator[str]:
    create_db(str(db_path))
    currency_dao = CurrencyDAO(str(db_path))
    currency_service = CurrencyService(currency_dao)
    exchange_rate_dao = ExchangeRateDAO(str(db_path))
    exchange_rate_service = ExchangeRateService(exchange_rate_dao)
    server_handler = create_handler(currency_service, exchange_rate_service)
    server = HTTPServer(("0.0.0.0", 0), server_handler)
    host, port = server.server_address

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://{host}:{port}"

    server.shutdown()
    thread.join()
    server.server_close()


@pytest.fixture
def currency_factory():
    def create_currency(code: str, without: list[str] | None = None) -> dict:
        currencies = {
            "USD": {
                "code": "USD",
                "name": "United States dollar",
                "sign": "$"
            },
            "RUB": {
                "code": "RUB",
                "name": "Russian ruble",
                "sign": "₽"
            },
            "EUR": {
                "code": "EUR",
                "name": "Euro",
                "sign": "€"
            }
        }

        currency = dict(currencies[code])

        if without:
            for key in without:
                currency.pop(key)

        return currency

    return create_currency


def assert_currencies_response(excepted: dict, received: dict):
    assert received["code"] == excepted["code"]
    assert received["name"] == excepted["name"]
    assert received["sign"] == excepted["sign"]
