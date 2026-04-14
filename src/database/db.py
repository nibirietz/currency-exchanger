import sqlite3
from decimal import Decimal

from src.dto.currency_dto import CurrencyResponse
from src.dto.exchange_rate_dto import ExchangeRateResponse
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

    def get_all_currencies(self) -> list[CurrencyResponse]:
        query = """SELECT * FROM currencies;"""
        currencies: list[CurrencyResponse] = [self._row_to_currency_response(row) for row in
                                              self.cursor.execute(query).fetchall()]
        return currencies

    def get_currency(self, code: str) -> CurrencyResponse | None:
        query = """SELECT * FROM currencies
                   WHERE code = ?;"""
        currency_row = self.cursor.execute(query, [code]).fetchone()
        if not currency_row:
            return None

        currency = self._row_to_currency_response(currency_row)

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

    def add_exchange_rates(self, base_currency_id: str, target_currency_id: str, rate: Decimal):
        # query = """INSERT INTO exchange_rates (base_currency_id, target_currency_id, rate)
        #            SELECT currency1.id, currency2.id, ?
        #            FROM currencies currency1, currencies currency2
        #            WHERE currency1.full_name = ? AND currency2.full_name = ?
        #            RETURNING exchange_rates.id, base_currency_id, target_currency_id, rate;"""
        # self.cursor.execute(query, (rate, base_currency_, target_currency_name))
        # self.connection.commit()
        pass

    def get_all_exchange_rates(self) -> list:
        query = f"""{SELECT_EXCHANGE_RATE_QUERY};"""
        exchange_rates = [self.exchange_rates_mapper.row_to_response(row) for row in self.cursor.execute(query)]
        return exchange_rates

    def _row_to_currency_response(self, row: sqlite3.Row) -> CurrencyResponse:
        return CurrencyResponse(
            id=row["id"],
            code=row["code"],
            name=row["full_name"],
            sign=row["sign"]
        )

    # def _row_to_exchange_rate(self, row: sqlite3.Row) -> ExchangeRates:
    #     return ExchangeRates(
    #         id=row["id"],
    #         base_currency_id=row["base_currency_id"],
    #         target_currency_id=row["target_currency_id"],
    #         rate=row["rate"]
    #     )
