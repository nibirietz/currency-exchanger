from collections.abc import Iterator
import sqlite3
from contextlib import contextmanager

from src.config import Config


@contextmanager
def db_session() -> Iterator[sqlite3.Cursor]:
    try:
        connection = sqlite3.connect(Config.DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
    except sqlite3.Error as e:
        raise e

    try:
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
