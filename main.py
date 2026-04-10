from http.server import HTTPServer

from src.config import Config
from src.database.create_database import create_db
from src.database.db import Database
from src.server import create_handler
from src.service import Service


def main():
    create_db()
    database = Database(Config.DATABASE_PATH)
    service = Service(database)
    server_handler = create_handler(service)
    server = HTTPServer(('0.0.0.0', 8080), server_handler)
    server.serve_forever()


if __name__ == '__main__':
    main()
