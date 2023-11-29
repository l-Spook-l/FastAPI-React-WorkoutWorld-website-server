from dotenv import load_dotenv
import os

# from main import app  # циклический импорт
# from fastapi.middleware.cors import CORSMiddleware  # для связи с фронтом


load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASSWORD_TEST = os.environ.get("DB_PASSWORD_TEST")
DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")

SECRET_KEY = os.environ.get("SECRET_KEY")

SMTP_USER_EMAIL = os.environ.get("SMTP_USER_EMAIL")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")


# CORS
# адреса фронта
# middleware - прослойка между запросом и обработкой (после запроса из фронта и перед обработкой в бэк)
# origins = [
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:3000",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # позволяем сайтам из списка обращаться к нам
#     allow_credentials=True,  # куки
#     # allow_methods=["*"],    # разрешаем все методы (get, post ...) но лучше все самому прописать
#     allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
#     # allow_headers=["*"], # разрешаем все headers (заголовки) но лучше все самому прописать
#     allow_headers=["Content-Type", "Set-Cookie:", "Authorization", "Accept-Control-Allow-Headers"],
# )
