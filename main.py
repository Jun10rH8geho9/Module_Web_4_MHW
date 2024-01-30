from server import ThreadedHTTPServer
from socket_server import SocketServer

def main():
    http_server = ThreadedHTTPServer('0.0.0.0', 3000)
    http_server.start()

    socket_server = SocketServer('0.0.0.0', 5000)
    socket_server.start()

    # Зупинка сервера при отриманні Ctrl+C
    try:
        while http_server.is_running and socket_server.is_running:
            pass
    except KeyboardInterrupt:
        print("Зупинка сервера...")
        http_server.stop()

        # Додатково перевіримо, чи сервер socket_server працює і зупинимо його
        if socket_server.is_running:
            socket_server.stop()

if __name__ == "__main__":
    main()