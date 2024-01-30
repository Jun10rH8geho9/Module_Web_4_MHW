import datetime
import json
import socket
import threading

#  Прийом та обробка даних через UDP-сокет
class SocketServer:
    def __init__(self, host='localhost', port=5000):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((host, port))
        self.is_running = True
    # Запускаємо основний цикл обробки даних в окремому потоці,
    def start(self):
        threading.Thread(target=self.run, daemon=True).start()

    # Приймаємо дані через UDP-сокет, декодуємо їх, та передає для збереження у файл методу save_to_file.Працює, доки прапорець is_running дорівнює True.
    def run(self):
        while self.is_running:
            data, addr = self.server.recvfrom(1024)
            message_data = data.decode('utf-8')
            self.save_to_file(message_data)

    #  Зупиняє сервер, встановлюючи прапорець is_running в False та закриваючи UDP-сокет.
    def stop(self):
        self.is_running = False
        self.server.close()
    # Обробляємо та зберігаємо отримані дані у файл. Завантажуємо поточні дані з файлу, додаємо нові дані та зберігаємо оновлені дані у форматі JSON.
    def save_to_file(self, message_data):
        try:
            # Завантажуємо поточні дані з файлу
            current_data = {}
            
            try:
                with open('storage/data.json', 'r') as f:
                    loaded_data = json.load(f)
                    if isinstance(loaded_data, dict):
                        current_data = loaded_data
            except FileNotFoundError:
                pass  # Якщо файл відсутній, продовжити з порожнім словником

            # print(f"Тип поточних даних: {type(current_data)}")

            # Парсинг даних вхідного повідомлення у форматі JSON
            try:
                parsed_data = json.loads(message_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return  # Не продовжувати, якщо декодування JSON завершилося невдало

            # Вставити завантажені дані у нове повідомлення
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            current_data[now] = parsed_data

            # Зберегти оновлені дані у файл
            with open('storage/data.json', 'w') as f:
                json.dump(current_data, f, indent=4)

        except Exception as e:
            print(f"Error while saving to file: {e}")
            raise ValueError(f"Error saving to file: {e}")