import sqlite3
from decimal import Decimal
from typing import Optional

from src.dto.currency_dto import CurrencyResponse
from src.dto.exchange_rate_dto import ExchangeRateResponse
from src.mappers.currency_mapper import CurrencyMapper
from src.mappers.exchange_rate_mapper import ExchangeRateMapper

SELECT_EXCHANGE_RATE_QUERY = """
SELECT exchange_rates.id,
       base_currency.id AS base_currency_id,
       base_currency.full_name AS base_currency_full_name,
       base_currency.code AS base_currency_code,
       base_currency.sign AS base_currency_sign,
       target_currency.id AS target_currency_id,
       target_currency.full_name AS target_currency_full_name,
       target_currency.code AS target_currency_code,
       target_currency.sign AS target_currency_sign,
       exchange_rates.rate
FROM exchange_rates 
JOIN currencies base_currency ON exchange_rates.base_currency_id = base_currency.id
JOIN currencies target_currency ON exchange_rates.target_currency_id = target_currency.id
"""


class Database:
    def __init__(self, path: str):
        try:
            self.connection = sqlite3.connect(path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        except Exception:
            raise Exception("Внутренняя ошибка.")
        self.exchange_rates_mapper = ExchangeRateMapper()
        self.currency_rates_mapper = CurrencyMapper()

    def get_all_currencies(self) -> list[CurrencyResponse]:
        query = """SELECT * FROM currencies;"""
        currencies: list[CurrencyResponse] = [self.currency_rates_mapper.row_to_response(row) for row in
                                              self.cursor.execute(query).fetchall()]
        return currencies

    def get_currency(self, code: str) -> Optional[CurrencyResponse]:
        query = """SELECT * FROM currencies
                   WHERE code = ?;"""
        currency_row = self.cursor.execute(query, [code]).fetchone()
        if not currency_row:
            return None

        currency = self.currency_rates_mapper.row_to_response(currency_row)

        return currency

    def add_currency(self, code: str, name: str, sign: str):
        query = """INSERT INTO currencies (code, full_name, sign) VALUES (?, ?, ?);"""
        try:
            self.cursor.execute(query, (code, name, sign))
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise sqlite3.IntegrityError("Все коды должны быть уникальны!")

    def get_exchange_rate_by_id(self, exchange_rate_id: int) -> ExchangeRateResponse:
        query = f"""{SELECT_EXCHANGE_RATE_QUERY}
                   WHERE exchange_rates.id = ?;"""
        exchange_rate_row = self.cursor.execute(query, [exchange_rate_id]).fetchone()
        return self.exchange_rates_mapper.row_to_response(exchange_rate_row)

    def add_exchange_rates(self, base_currency_code: str, target_currency_code: str, rate: Decimal):
        query = """INSERT INTO exchange_rates (base_currency_id, target_currency_id, rate)
                   SELECT base_currency.id, target_currency.id, ?
                   FROM currencies base_currency CROSS JOIN currencies target_currency
                   WHERE base_currency.code = ? AND target_currency.code = ?;"""
        self.cursor.execute(query, (str(rate), base_currency_code, target_currency_code))
        self.connection.commit()

        return self.cursor.lastrowid

    def get_all_exchange_rates(self) -> list:
        query = f"""{SELECT_EXCHANGE_RATE_QUERY};"""
        exchange_rates = [self.exchange_rates_mapper.row_to_response(row) for row in
                          self.cursor.execute(query).fetchall()]
        return exchange_rates

    def get_exchange_rate(self, base_code: str, target_code: str) -> Optional[ExchangeRateResponse]:
        query = f"""{SELECT_EXCHANGE_RATE_QUERY}
                    WHERE base_currency_code = ? AND target_currency_code = ?;"""
        exchange_rate_row = self.cursor.execute(query, (base_code, target_code)).fetchone()
        if not exchange_rate_row:
            return None

        return self.exchange_rates_mapper.row_to_response(exchange_rate_row)
