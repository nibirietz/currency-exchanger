from http.server import HTTPServer

from src.config import Config
from src.database.create_database import create_db
from src.database.currency_dao import CurrencyDAO
from src.database.exchange_rate_dao import ExchangeRateDAO
from src.server import create_handler
from src.services.currency_service import CurrencyService
from src.services.exchange_rate_service import ExchangeRateService
from src.services.exchange_service import ExchangeService


def main():
    create_db(Config.DATABASE_PATH)
    currency_dao = CurrencyDAO(Config.DATABASE_PATH)
    currency_service = CurrencyService(currency_dao)
    exchange_rate_dao = ExchangeRateDAO(Config.DATABASE_PATH)
    exchange_rate_service = ExchangeRateService(exchange_rate_dao)
    exchange_service = ExchangeService(currency_dao, exchange_rate_dao)
    server_handler = create_handler(currency_service, exchange_rate_service, exchange_service)
    server = HTTPServer(("0.0.0.0", 8080), server_handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
