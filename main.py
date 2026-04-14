from http.server import HTTPServer

from src.config import Config
from src.database.create_database import create_db
from src.database.currency_dao import CurrencyDAO
from src.database.db import ExchangeRateDAO
from src.mappers.currency_mapper import CurrencyMapper
from src.mappers.exchange_rate_mapper import ExchangeRateMapper
from src.server import create_handler
from src.service import Service


def main():
    create_db()
    currency_mapper = CurrencyMapper()
    currency_dao = CurrencyDAO(currency_mapper)
    exchange_rate_mapper = ExchangeRateMapper()
    exchange_rate_dao = ExchangeRateDAO(exchange_rate_mapper)
    service = Service(currency_dao, exchange_rate_dao)
    server_handler = create_handler(service)
    server = HTTPServer(('0.0.0.0', 8080), server_handler)
    server.serve_forever()


if __name__ == '__main__':
    main()
