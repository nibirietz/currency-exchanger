import sqlite3


def create_db(db_path: str):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    currency_query = """CREATE TABLE IF NOT EXISTS currencies(
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             code VARCHAR UNIQUE,
                             full_name VARCHAR,
                             sign VARCHAR
                         );"""
    exchange_query = """CREATE TABLE IF NOT EXISTS exchange_rates(
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             base_currency_id INTEGER, 
                             target_currency_id INTEGER,
                             rate DECIMAL(6),
                             FOREIGN KEY(base_currency_id) REFERENCES currencies(id),
                             FOREIGN KEY(target_currency_id) REFERENCES currencies(id),
                             UNIQUE (base_currency_id, target_currency_id)
                        );"""

    cursor.execute(currency_query)
    cursor.execute(exchange_query)
    connection.close()


if __name__ == "__main__":
    create_db()
