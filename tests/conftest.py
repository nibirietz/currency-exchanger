import threading
from collections.abc import Callable, Generator, Mapping
from http.server import HTTPServer
from pathlib import Path

import pytest

from src.database.create_database import create_db
from src.database.currency_dao import CurrencyDAO
from src.database.exchange_rate_dao import ExchangeRateDAO
from src.server import create_handler
from src.services.currency_service import CurrencyService
from src.services.exchange_rate_service import ExchangeRateService
from src.services.exchange_service import ExchangeService


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    return tmp_path / "test.sqlite"


@pytest.fixture
def currency_dao(db_path: Path) -> CurrencyDAO:
    return CurrencyDAO(db_path)


@pytest.fixture
def exchange_rate_dao(db_path: Path) -> ExchangeRateDAO:
    return ExchangeRateDAO(db_path)


@pytest.fixture
def server_url(db_path: Path) -> Generator[str]:
    create_db(db_path)
    currency_dao = CurrencyDAO(db_path)
    currency_service = CurrencyService(currency_dao)
    exchange_rate_dao = ExchangeRateDAO(db_path)
    exchange_rate_service = ExchangeRateService(exchange_rate_dao)
    exchange_service = ExchangeService(currency_dao, exchange_rate_dao)
    server_handler = create_handler(
        currency_service, exchange_rate_service, exchange_service
    )
    server = HTTPServer(("0.0.0.0", 0), server_handler)
    host, port = server.server_address

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://{host}:{port}"

    server.shutdown()
    thread.join()
    server.server_close()


def create_currency(code: str, without: list[str] | None = None) -> dict[str, str]:
    currencies = {
        "USD": {"code": "USD", "name": "United States dollar", "sign": "$"},
        "RUB": {"code": "RUB", "name": "Russian ruble", "sign": "₽"},
        "EUR": {"code": "EUR", "name": "Euro", "sign": "€"},
    }

    currency = dict(currencies[code])

    if without:
        for key in without:
            _ = currency.pop(key)

    return currency


def assert_currencies_response(
    excepted: dict[str, object], received: dict[str, object]
):
    assert received["code"] == excepted["code"]
    assert received["name"] == excepted["name"]
    assert received["sign"] == excepted["sign"]
