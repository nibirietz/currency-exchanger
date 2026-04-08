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

    def post_currency(self, currency_post: CurrencyPost):
        pass
