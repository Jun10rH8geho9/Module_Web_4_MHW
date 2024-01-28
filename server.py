import datetime
import json
import signal
import threading
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer

mimetypes.init()

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            mime_type, _ = mimetypes.guess_type(self.path)
            file_to_open = open(self.path[1:], 'rb').read()
            self.send_response(200)
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
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            if post_data:
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()

                try:
                    message = json.loads(post_data.decode('utf-8'))
                except json.JSONDecodeError as json_error:
                    raise ValueError(f"Помилка розпізнавання JSON: {json_error}")

                with open('storage/data.json', 'a') as f:
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                    json.dump({now: message}, f)
                    f.write('\n')

                self.wfile.write(bytes("POST-запит успішно оброблено", 'utf-8'))
            else:
                raise ValueError("Порожні дані JSON")
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(f"Помилка обробки POST-запиту: {str(e)}", 'utf-8'))

class ThreadedHTTPServer(object):
    def __init__(self, host, port):
        self.server = HTTPServer((host, port), MyHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.is_running = True

        # Додаємо обробник для сигналу Ctrl+C
        signal.signal(signal.SIGINT, self.shutdown)

    def start(self):
        self.thread.start()

    def wait_for_thread(self):
        self.thread.join()

    def stop(self):
        self.server.shutdown()
        self.wait_for_thread()

    def shutdown(self, signum, frame):
        print('Зупинка сервера...')
        self.is_running = False
        self.server.shutdown()