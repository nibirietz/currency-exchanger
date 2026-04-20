from http.server import HTTPServer

from src.database.create_database import create_db
from src.database.currency_dao import CurrencyDAO
from src.database.exchange_rate_dao import ExchangeRateDAO
from src.mappers.currency_mapper import CurrencyMapper
from src.mappers.exchange_rate_mapper import ExchangeRateMapper
from src.server import create_handler
from src.services.currency_service import CurrencyService
from src.services.exchange_rate_service import ExchangeRateService


def main():
    create_db()
    currency_mapper = CurrencyMapper()
    currency_dao = CurrencyDAO(currency_mapper)
    currency_service = CurrencyService(currency_dao)
    exchange_rate_mapper = ExchangeRateMapper()
    exchange_rate_dao = ExchangeRateDAO(exchange_rate_mapper)
    exchange_rate_service = ExchangeRateService(exchange_rate_dao)
    server_handler = create_handler(currency_service, exchange_rate_service)
    server = HTTPServer(("0.0.0.0", 8080), server_handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
