# КОД ИЗ ДОКУМЕНТАЦИИ только поменял - IntegerIDMixin
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, exceptions, models, schemas
from fastapi_users import IntegerIDMixin  # для последовательного id для пользователя

from .models import User
from .utils import get_user_db
from fastapi_users.jwt import generate_jwt
from src.config import SECRET_KEY


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    # разные фун-ии
    # после регистрации делаем что-то
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    # Забыл пароль
    async def forgot_password(
        self, user: models.UP, request: Optional[Request] = None
    ) -> str:

        if not user.is_active:
            raise exceptions.UserInactive()

        token_data = {
            "sub": str(user.id),
            "password_fgpt": self.password_helper.hash(user.hashed_password),
            "aud": self.reset_password_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.reset_password_token_secret,
            self.reset_password_token_lifetime_seconds,
        )
        await self.on_after_forgot_password(user, token, request)
        return token

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id}, email {user.email} has forgot their password. Reset token: {token}")

    # фун-я из класса BaseUserManager, мы ее немного меняем
    # фун-я создает пользователя
    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 2  # при регистрации выставляем пользователю 2ю роль

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
