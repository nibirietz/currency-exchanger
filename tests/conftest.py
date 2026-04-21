import threading
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
