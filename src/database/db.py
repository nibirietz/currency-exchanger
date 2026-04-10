import sqlite3
from decimal import Decimal

from src.database.models import Currency, ExchangeRates


class Database:
    def __init__(self, path: str):
        try:
            self.connection = sqlite3.connect(path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        except Exception:
            pass

    def get_all_currencies(self) -> list[Currency]:
        query = """SELECT * FROM currencies;"""
        currencies: list[Currency] = [self._row_to_currency(row) for row in self.cursor.execute(query).fetchall()]
        return currencies

    def get_currency(self, code: str) -> Currency | None:
        query = """SELECT * FROM currencies
                   WHERE code = ?;"""
        currency_row = self.cursor.execute(query, [code]).fetchall()
        if not currency_row:
            return None

        currency = self._row_to_currency(currency_row[0])

        return currency

    def add_currency(self, code: str, name: str, sign: str):
        query = """INSERT INTO currencies (code, full_name, sign) VALUES (?, ?, ?);"""
        try:
            self.cursor.execute(query, (code, name, sign))
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise sqlite3.IntegrityError("Все коды должны быть уникальны!")

    def add_exchange_rates(self, base_currency_name: int, target_currency_name: int, rate: Decimal):
        # query = """INSERT INTO exchange_rates (base_currency_id, target_currency_id, rate) VALUES (?, ?, ?);"""
        # self.cursor.execute(query, (base_currency_id, target_currency_id, rate))
        # self.connection.commit()
        pass

    def get_all_exchange_rates(self) -> list[ExchangeRates]:
        query = """SELECT * FROM exchange_rates;"""
        exchange_rates: list[ExchangeRates] = [self._row_to_exchange_rate(row) for row in
                                               self.cursor.execute(query).fetchall()]
        return exchange_rates

    def _row_to_currency(self, row: sqlite3.Row) -> Currency:
        return Currency(
            id=row["id"],
            code=row["code"],
            full_name=row["full_name"],
            sign=row["sign"]
        )

    def _row_to_exchange_rate(self, row: sqlite3.Row) -> ExchangeRates:
        return ExchangeRates(
            id=row["id"],
            base_currency_id=row["base_currency_id"],
            target_currency_id=row["target_currency_id"],
            rate=row["rate"]
        )
