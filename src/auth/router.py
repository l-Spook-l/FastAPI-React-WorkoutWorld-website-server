from fastapi import APIRouter

from .base_config import auth_backend, fastapi_users
from .schemas import UserRead, UserCreate, UserUpdate

router = APIRouter()

# авторизация
router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"],
)
# регистрация
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth/jwt", tags=["auth"],
)
# сброс пароля
router.include_router(
    fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"],
)
# Обновление данных о пользователе
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"],
)

