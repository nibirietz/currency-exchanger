from src.server import Server


def main():
    server = Server('', 8080)
    server.run()


if __name__ == '__main__':
    main()
