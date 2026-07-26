import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def db_session(db_path: str) -> Iterator[sqlite3.Cursor]:
    try:
        connection = sqlite3.connect(db_path)
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
