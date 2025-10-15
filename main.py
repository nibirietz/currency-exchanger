from src.server import Server
from src.service import Service


def main():
    server = Server('', 8080)
    server.run()


if __name__ == '__main__':
    main()
