from fastapi import APIRouter, Depends

from .base_config import auth_backend, fastapi_users
from .models import User
from .schemas import UserRead, UserCreate, UserUpdate, PasswordResetRequest, PasswordReset
from fastapi.exceptions import HTTPException
from .manager import UserManager
from sqlalchemy import select, insert, update, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from .utils import get_user_db, send_token_by_email

router = APIRouter()

# авторизация
router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"],
)
# регистрация
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"],
)
# сброс пароля
router.include_router(
    fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"],
)
# Обновление данных о пользователе
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"],
)


@router.post("/request-password-reset")
async def request_password_reset(request: PasswordResetRequest, session: AsyncSession = Depends(get_async_session)):
    # Находим пользователя в базе данных по email
    query_user = await session.execute(select(User).filter(User.email == request.email))
    user = query_user.one()[0]
    print('user1', user)

    if not user:
        raise HTTPException(status_code=404, detail="Workout not found")

    user_manager = UserManager(get_user_db)
    reset_token = await user_manager.forgot_password(user)
    # Отправьте reset_token пользователю (например, по почте)
    print('token', reset_token)
    await send_token_by_email(user.email, reset_token)
    return {"message": "If the email exists, a password reset link has been sent.", 'token': reset_token}


# @router.post("/reset-password")
# async def reset_password(reset_data: PasswordReset):
#     print('token', reset_data.token)
#     print('new_password', reset_data.new_password)
#     # Измените пароль пользователя в базе данных
#     user_manager = UserManager(get_user_db)
#     user = await user_manager.reset_password(token=reset_data.token, password=reset_data.new_password)
#
#     if user:
#         return {"message": "Password has been reset."}
#     else:
#         raise HTTPException(status_code=400, detail="Invalid or expired token.")
