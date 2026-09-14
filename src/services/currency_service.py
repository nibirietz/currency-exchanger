import sqlite3

from src.database.currency_dao import CurrencyDAO
from src.dto.currency_dto import CurrencyRequest, CurrencyResponse
from src.exceptions import (
    CurrencyAlreadyExistsError,
    CurrencyNotFoundError,
)
from src.mappers.currency_mapper import CurrencyMapper


class CurrencyService:
    def __init__(self, currency_dao: CurrencyDAO):
        self.currency_dao = currency_dao

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
            last_row_id = self.currency_dao.add_currency(
                currency_post.code, currency_post.name, currency_post.sign
            )
            return CurrencyMapper.request_to_response(currency_post, last_row_id)
        except sqlite3.IntegrityError:
            raise CurrencyAlreadyExistsError(
                f"Валюта с кодом {currency_post.code} существует."
            )
