# Базовый образ Python
FROM python:3.10-slim

RUN mkdir /fastapi_app

# Рабочая директория в контейнере
WORKDIR /fastapi_app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем все файлы в контейнер
COPY . .

RUN chmod a+x docker/*.sh

#WORKDIR   # указывать если в корне то так, есть папка то - src

# Команда для запуска FastAPI
#CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

