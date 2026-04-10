import sqlite3

from src.database.db import Database
from src.database.models import Currency, ExchangeRates
from src.dto.currency_post_dto import CurrencyPost


class Service:
    def __init__(self, database: Database):
        self.database = database

    def get_all_currencies(self) -> list[Currency]:
        currencies = self.database.get_all_currencies()
        return currencies

    def get_currency(self, currency_name: str) -> Currency:
        currency = self.database.get_currency(currency_name)
        if not currency:
            raise CurrencyNotFoundError("Валюта не найдена.")
        return currency

    def add_currency(self, currency_post: CurrencyPost):
        try:
            self.database.add_currency(currency_post.code, currency_post.name, currency_post.sign)
        except sqlite3.IntegrityError:
            raise CurrencyAlreadyExistsError(f"Валюта с кодом {currency_post.code} существует.")

    def get_all_exchange_rates(self) -> ExchangeRates:
        return


class CurrencyAlreadyExistsError(Exception):
    pass


class CurrencyNotFoundError(Exception):
    pass
