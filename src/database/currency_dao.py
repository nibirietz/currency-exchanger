import sqlite3
from typing import Optional

from src.database.base_dao import BaseDAO
from src.dto.currency_dto import CurrencyResponse
from src.mappers.currency_mapper import CurrencyMapper
from src.mappers.exchange_rate_mapper import ExchangeRateMapper

SELECT_CURRENCY_QUERY = """SELECT id, full_name, code, sign FROM currencies"""


class CurrencyDAO(BaseDAO):
    def __init__(self, currency_rates_mapper: CurrencyMapper):
        self.currency_rates_mapper = currency_rates_mapper

    def get_all_currencies(self) -> list[CurrencyResponse]:
        query = f"""{SELECT_CURRENCY_QUERY};"""
        currencies: list[CurrencyResponse] = [self.currency_rates_mapper.row_to_response(row) for row in
                                              self._execute_all(query)]
        return currencies

    def get_currency(self, code: str) -> Optional[CurrencyResponse]:
        query = f"""{SELECT_CURRENCY_QUERY}
                   WHERE code = ?;"""
        currency_row = self._execute_one(query, code)
        if not currency_row:
            return None

        currency = self.currency_rates_mapper.row_to_response(currency_row)

        return currency

    def add_currency(self, code: str, name: str, sign: str):
        query = """INSERT INTO currencies (code, full_name, sign) VALUES (?, ?, ?);"""
        try:
            self._execute(query, (code, name, sign))
        except sqlite3.IntegrityError:
            raise sqlite3.IntegrityError("Все коды должны быть уникальны!")
