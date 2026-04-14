import sqlite3
from decimal import Decimal

from src.database.db import Database
from src.dto.currency_dto import CurrencyPost, CurrencyResponse


class Service:
    def __init__(self, database: Database):
        self.database = database

    def get_all_currencies(self) -> list[CurrencyResponse]:
        currencies = self.database.get_all_currencies()
        return currencies

    def get_currency(self, currency_name: str) -> CurrencyResponse:
        currency = self.database.get_currency(currency_name)
        if not currency:
            raise CurrencyNotFoundError("Валюта не найдена.")
        return currency

    def add_currency(self, currency_post: CurrencyPost):
        try:
            self.database.add_currency(currency_post.code, currency_post.name, currency_post.sign)
        except sqlite3.IntegrityError:
            raise CurrencyAlreadyExistsError(f"Валюта с кодом {currency_post.code} существует.")

    # def add_exchange_rate(self, base_currency_name: str, target_currency_name: str, rate: Decimal):
    #     self.database.add_exchange_rates(base_currency_name, target_currency_name, rate)

    # def get_all_exchange_rates(self) -> ExchangeRates:
    #     return


class CurrencyAlreadyExistsError(Exception):
    pass


class CurrencyNotFoundError(Exception):
    pass
