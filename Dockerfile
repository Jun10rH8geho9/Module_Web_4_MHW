# Використовуйте офіційний образ Python
FROM python:3.12

# Створюємо каталог для додатку
WORKDIR /app

# Копіюємо файли додатку в контейнер
COPY error.html /app/error.html
COPY logo.png /app/logo.png
COPY message.html /app/message.html
COPY index.html /app/index.html
COPY main.py /app/main.py
COPY client.py /app/client.py
COPY server.py /app/server.py
COPY socket_server.py /app/socket_server.py

# Перевіряємо існування каталогу storage та файлу data.json
RUN mkdir -p /app/storage
RUN touch /app/storage/data.json

# Запуск додатку
CMD ["python", "main.py"]