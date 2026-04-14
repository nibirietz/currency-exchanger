import sqlite3
from decimal import Decimal

from src.database.currency_dao import CurrencyDAO
from src.database.exchange_rate_dao import ExchangeRateDAO
from src.dto.currency_dto import CurrencyRequest, CurrencyResponse
from src.dto.exchange_rate_dto import ExchangeRateResponse
from src.exceptions import CurrencyAlreadyExistsError, CurrencyNotFoundError, ExchangeRateNotFoundError, \
    ExchangeRateAlreadyExistsError
from src.mappers.currency_mapper import CurrencyMapper


class Service:
    def __init__(self, currency_dao: CurrencyDAO, exchange_rate_dao: ExchangeRateDAO):
        self.currency_dao = currency_dao
        self.exchange_rate_dao = exchange_rate_dao

    def get_all_currencies(self) -> list[CurrencyResponse]:
        currencies = self.currency_dao.get_all_currencies()
        return currencies

    def get_currency(self, currency_code: str) -> CurrencyResponse:
        currency = self.currency_dao.get_currency(currency_code)
        if not currency:
            raise CurrencyNotFoundError("Валюта не найдена.")
        return currency

    def add_currency(self, currency_post: CurrencyRequest) -> CurrencyResponse:
        try:
            last_row_id = self.currency_dao.add_currency(currency_post.code, currency_post.name, currency_post.sign)
            return CurrencyMapper.request_to_response(currency_post, last_row_id)
        except sqlite3.IntegrityError:
            raise CurrencyAlreadyExistsError(f"Валюта с кодом {currency_post.code} существует.")

    def add_exchange_rate(self, base_currency_name: str, target_currency_name: str,
                          rate: Decimal) -> ExchangeRateResponse:
        try:
            inserted_id = self.exchange_rate_dao.add_exchange_rates(base_currency_name, target_currency_name, rate)
            if inserted_id == 0:
                raise CurrencyNotFoundError("Одна(или обе) валюта из валютной пары не существует.")
        except sqlite3.IntegrityError:
            raise ExchangeRateAlreadyExistsError("Валютная пара уже существует.")

        return self.exchange_rate_dao.get_exchange_rate_by_id(inserted_id)

    def get_all_exchange_rates(self) -> list[ExchangeRateResponse]:
        exchange_rates: list[ExchangeRateResponse] = self.exchange_rate_dao.get_all_exchange_rates()
        return exchange_rates

    def get_exchange_rate(self, base_code: str, target_code: str) -> ExchangeRateResponse:
        exchange_rate = self.exchange_rate_dao.get_exchange_rate(base_code, target_code)
        if not exchange_rate:
            raise ExchangeRateNotFoundError("Обменный курс не найден.")

        return exchange_rate

    def patch_exchange_rate(self, base_code: str, target_code: str, rate: Decimal) -> ExchangeRateResponse:
        self.exchange_rate_dao.patch_exchange_rate(base_code, target_code, rate)
        exchange_rate = self.exchange_rate_dao.get_exchange_rate(base_code, target_code)
        if not exchange_rate:
            raise ExchangeRateNotFoundError("Обменный курс не найден.")

        return exchange_rate
