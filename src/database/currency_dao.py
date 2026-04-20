import sqlite3
from typing import Optional

from src.database.base_dao import BaseDAO
from src.dto.currency_dto import CurrencyResponse
from src.mappers.currency_mapper import CurrencyMapper

SELECT_CURRENCY_QUERY = """SELECT id, full_name, code, sign FROM currencies"""


class CurrencyDAO(BaseDAO):
    def get_all_currencies(self) -> list[CurrencyResponse]:
        query = f"""{SELECT_CURRENCY_QUERY};"""
        currencies: list[CurrencyResponse] = [
            CurrencyMapper.row_to_response(row) for row in self._execute_all(query)
        ]
        return currencies

    def get_currency(self, code: str) -> Optional[CurrencyResponse]:
        query = f"""{SELECT_CURRENCY_QUERY}
                   WHERE code = ?;"""
        currency_row = self._execute_one(query, (code,))
        if not currency_row:
            return None

        currency = CurrencyMapper.row_to_response(currency_row)

        return currency

    def add_currency(self, code: str, name: str, sign: str):
        query = """INSERT INTO currencies (code, full_name, sign) VALUES (?, ?, ?);"""
        try:
            last_row_id = self._execute_returning_last_row_id(query, (code, name, sign))
            return last_row_id
        except sqlite3.IntegrityError:
            raise sqlite3.IntegrityError("Все коды должны быть уникальны!")
