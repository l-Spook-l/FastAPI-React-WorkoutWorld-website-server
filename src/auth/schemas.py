# Это как сериализаторы и валидаторы
from typing import Optional

from fastapi_users import schemas


# был pass, но для понимая пишем то что внутри
# читаем пользователя
class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    first_name: str
    second_name: str
    email: str
    phone: int
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        # orm_mode = True
        from_attributes = True


# создаем пользователя
class UserCreate(schemas.BaseUserCreate):
    username: str
    first_name: str
    second_name: str
    email: str
    phone: int
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

# если надо обновить
# class UserUpdate(schemas.BaseUserUpdate):
#     pass
