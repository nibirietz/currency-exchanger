import sqlite3
from abc import ABC
from typing import Optional

from src.database.db_session import db_session


class BaseDAO(ABC):
    @staticmethod
    def _execute(query: str, params: Optional[tuple] = None):
        with db_session() as cursor:
            cursor.execute(query, params or ())

    @staticmethod
    def _execute_one(query: str, params: Optional[tuple] = None) -> sqlite3.Row:
        with db_session() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    @staticmethod
    def _execute_all(query: str, params: Optional[tuple] = None) -> list[sqlite3.Row]:
        with db_session() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    @staticmethod
    def _execute_returning_last_row_id(query: str, params: Optional[tuple] = None) -> int:
        with db_session() as cursor:
            cursor.execute(query, params or ())

            if cursor.lastrowid is None:
                raise RuntimeError("Вставка не удалась.")
            else:
                return cursor.lastrowid
