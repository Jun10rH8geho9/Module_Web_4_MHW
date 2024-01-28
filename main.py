from server import ThreadedHTTPServer


def main():
    http_server = ThreadedHTTPServer('localhost', 3000)
    http_server.start()

    # Зупинка сервера при отриманні Ctrl+C
    try:
        while http_server.is_running:
            pass
    except KeyboardInterrupt:
        print("Зупинка сервера...")
        http_server.stop()

if __name__ == "__main__":
    main()