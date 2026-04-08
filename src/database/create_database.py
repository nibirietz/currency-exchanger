import sqlite3

from src.config import Config


def create_db():
    connection = sqlite3.connect("" + Config.DATABASE_PATH)
    cursor = connection.cursor()
    currency_query = """CREATE TABLE IF NOT EXISTS currencies(
                             id INTEGER PRIMARY KEY,
                             code VARCHAR,
                             full_name VARCHAR,
                             sign VARCHAR
                         );"""
    exchange_query = """CREATE TABLE IF NOT EXISTS exchange_rates(
                             id INTEGER PRIMARY KEY,
                             base_currency_id INTEGER, 
                             target_currency_id INTEGER,
                             rate DECIMAL(6),
                             FOREIGN KEY(base_currency_id) REFERENCES currencies(id),
                             FOREIGN KEY(target_currency_id) REFERENCES currencies(id)
                        );"""

    cursor.execute(currency_query)
    cursor.execute(exchange_query)
    connection.close()


if __name__ == "__main__":
    create_db()
