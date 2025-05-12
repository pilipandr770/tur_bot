# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка pipenv или poetry не требуется, используем requirements.txt

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Установка зависимостей
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Создание папки для изображений, если её нет
RUN mkdir -p /app/static/images

# Переменные окружения (можно также передавать через docker-compose)
ENV PYTHONUNBUFFERED=1

# Запуск приложения
CMD ["python", "run.py"]
