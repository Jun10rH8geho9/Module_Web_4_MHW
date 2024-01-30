import mimetypes
import json
import socket
import signal
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer


# Встановлюємо стандартні типи MIME
mimetypes.init()

# Обробку HTTP-запитань
class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            # MIME-тип на основі розширення файлу
            mime_type, _ = mimetypes.guess_type(self.path)
            # file_to_open = open(self.path[1:], 'rb').read()
            file_path = './' + self.path
            
                # Відкриття та читання файлу
            try:
                with open(file_path, 'rb') as file:
                    file_to_open = file.read()
            except FileNotFoundError:
                file_to_open = b'File not found'
            self.send_response(200)

            # Встановлюємо заголовок Content-Type
            self.send_header('Content-Type', mime_type)
            self.end_headers()
            self.wfile.write(file_to_open)
        except:
            file_to_open = "File not found"
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))

    
    # Обробка форми
    def do_POST(self):
        size = self.headers.get("Content-Length")
        post_data = self.rfile.read(int(size))
        
        try:
            if post_data:
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                print("Отримані дані з POST-запиту:", post_data)

                try:
                    data_parse = urllib.parse.unquote_plus(post_data.decode('utf-8'))
                    # Створюємо словник
                    data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
                    # print(data_dict)
                    message_data = json.dumps(data_dict)
                except json.JSONDecodeError as json_error:
                    raise ValueError(f"Помилка розпізнавання JSON: {json_error}")

                # Тут можна вивести повідомлення перед збереженням у файл
                print("Отримано нове повідомлення:", message_data)

                # Відправляємо дані на Socket сервер для обробки
                self.send_to_socket_server(message_data)
                
                self.wfile.write(bytes("POST-запит успішно оброблено", 'utf-8'))
            else:
                raise ValueError("Порожні дані JSON")
        except Exception as e:
            self.send_response(500)
            self.send_header('Location', '/')
            self.end_headers()
            self.wfile.write(bytes(f"Помилка обробки POST-запиту: {str(e)}", 'utf-8'))
    
    # Відправка данних на Socket сервер для обробки
    def send_to_socket_server(self, message_data):
        try:
            # Створюємо сокет
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Відправляємо дані на Socket сервер
            client.sendto(message_data.encode('utf-8'), ('localhost', 5000))
        except Exception as e:
            print(f"Помилка при відправці на Socket сервер: {e}")
            raise ValueError(f"Помилка при відправці на Socket сервер: {e}")
# Створення HTTP-сервера
class ThreadedHTTPServer(object):
    def __init__(self, host, port):
        self.server = HTTPServer((host, port), MyHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.is_running = True

        # Додаємо обробник для сигналу Ctrl+C
        signal.signal(signal.SIGINT, self.shutdown)

    # Запускаємо сервер у окремому потоці.
    def start(self):
        self.thread.start()
    # """Очікуємо завершення роботи потока сервера.
    def wait_for_thread(self):
        self.thread.join()
    # Зупиняємо сервер та чекає завершення роботи потока.
    def stop(self):
        self.server.shutdown()
        self.wait_for_thread()
    # Обробляє сигнал зупинки (Ctrl+C)
    def shutdown(self, signum, frame):
        print('Зупинка сервера...')
        self.is_running = False
        self.server.shutdown()