import sqlite3

from src.database.models import Currency


class Database:
    def __init__(self, path: str):
        try:
            self.connection = sqlite3.connect(path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        except:
            pass

    def get_all_currencies(self) -> list[Currency]:
        query = """SELECT * FROM currencies;"""
        currencies: list[Currency] = [self._row_to_currency(row) for row in self.cursor.execute(query).fetchall()]
        return currencies

    def _row_to_currency(self, row: sqlite3.Row):
        return Currency(
            id=row["id"],
            code=row["code"],
            full_name=row["full_name"],
            sign=row["sign"]
        )
