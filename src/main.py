from fastapi import FastAPI, Request, Depends
import uvicorn
from fastapi.exceptions import HTTPException

from src.auth.models import User
# from .auth.schemas import UserRead, UserCreate, UserUpdate
# from .auth.base_config import auth_backend, fastapi_users, current_user
from .auth.base_config import current_user
from .workouts.router import router as router_workout
from .auth.router import router as router_user
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware  # для связи с фронтом
import time

app = FastAPI(
    title="Workout App"
)

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     # start_time = time.time()
#
#     # Просмотр данных, отправленных на сервер
#     try:
#         data = await request.json()
#         print('Data sent to server:', data)
#     except:
#         print('что о нетак', request)
#
#
#     response = await call_next(request)
#
#     # process_time = time.time() - start_time
#     # response.headers["X-Process-Time"] = str(process_time)
#
#     return response


# Подключение media files
app.mount("/media", StaticFiles(directory="src/media"), name="media")


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    # return f"Hello, {user.email}"
    return user


# роутер для работы с пользователем
app.include_router(router_user)
# новый роутер для тренировок
app.include_router(router_workout)


# CORS
# middleware - прослойка между запросом и обработкой (после запроса из фронта и перед обработкой в бэк)
origins = [
    # адреса фронта
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # позволяем сайтам из списка обращаться к нам
    allow_credentials=True,  # куки
    # allow_methods=["*"],    # разрешаем все методы (get, post ...) но лучше все самому прописать
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],  # разрешаем все headers (заголовки) но лучше все самому прописать
    # allow_headers=["Content-Type", "Set-Cookie:", "Authorization", "Access-Control-Allow-Headers"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)