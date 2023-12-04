# Это как сериализаторы и валидаторы
from typing import Optional

from fastapi_users import schemas
from pydantic import Field  # помогает валидировать данные
from pydantic import BaseModel


# был pass, но для понимая пишем то что внутри
# читаем пользователя
class UserRead(schemas.BaseUser[int]):
    id: int
    first_name: str
    last_name: str
    # email: str
    phone: str = None
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        # orm_mode = True
        from_attributes = True


# создаем пользователя
class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    # email: str
    phone: str
    password: str = Field(min_length=8)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


# если надо обновить
# некоторые поля уже есть в BaseUserUpdate
class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


# Запрос на сброс пароля
class PasswordResetRequest(BaseModel):
    email: str


# Сброс пароля
class PasswordReset(BaseModel):
    token: str
    new_password: str


class SendMessageAdmin(BaseModel):
    name: str
    email: str
    message: str
