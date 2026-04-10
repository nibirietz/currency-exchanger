from src.database.db import Database
from src.database.models import Currency
from src.dto.currency_post_dto import CurrencyPost


class Service:
    def __init__(self, database: Database):
        self.database = database

    def get_all_currencies(self) -> list[Currency]:
        raw_currencies = self.database.get_all_currencies()
        return raw_currencies

    def get_currency(self, currency_name: str) -> dict:
        return {
            "id": 1,
            "name": "Rouble",
            "code": "RUB",
            "sign": "₽",
        }

    def add_currency(self, currency_post: CurrencyPost):
        self.database.add_currency(currency_post.code, currency_post.name, currency_post.sign)
