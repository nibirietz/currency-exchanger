from src.dto.currency_post_dto import CurrencyPost


class Service:
    def __init__(self, database):
        self.database = database

    def get_currencies(self) -> list[dict]:
        return [
            {
                "id": 1,
                "name": "Rouble",
                "code": "RUB",
                "sign": "₽",
            },
            {
                "id": 2,
                "name": "Euro",
                "code": "EUR",
                "sign": "€"
            }
        ]

    def get_currency(self, currency_name: str) -> dict:
        return {
            "id": 1,
            "name": "Rouble",
            "code": "RUB",
            "sign": "₽",
        }

    def post_currency(self, currency_post: CurrencyPost):
        pass
