import sqlite3
from abc import ABC
from typing import Optional

from src.database.db_session import db_session


class BaseDAO(ABC):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _execute(self, query: str, params: Optional[tuple] = None):
        with db_session(self.db_path) as cursor:
            cursor.execute(query, params or ())

    def _execute_one(self, query: str, params: Optional[tuple] = None) -> sqlite3.Row:
        with db_session(self.db_path) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def _execute_all(self, query: str, params: Optional[tuple] = None) -> list[sqlite3.Row]:
        with db_session(self.db_path) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def _execute_returning_last_row_id(self, query: str, params: Optional[tuple] = None) -> int:
        with db_session(self.db_path) as cursor:
            cursor.execute(query, params or ())

            if cursor.lastrowid is None:
                raise RuntimeError("Вставка не удалась.")
            else:
                return cursor.lastrowid

    def _execute_and_return_rowcount(self, query: str, params: tuple | None = None) -> int:
        with db_session(self.db_path) as cursor:
            cursor.execute(query, params or ())
            return cursor.rowcount
