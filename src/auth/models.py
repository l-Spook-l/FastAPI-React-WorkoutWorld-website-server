# Ну это модели
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from fastapi_users.db import SQLAlchemyBaseUserTable

from src.database import Base
# from src.workouts.models import Workout, Set


class Role(Base):
    __tablename__ = "role_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(length=99), nullable=False)
    # permissions: Mapped[JSON] = mapped_column(JSON, nullable=True)

    # тут список потому что много пользователей будет
    user: Mapped[list["User"]] = relationship(back_populates="role")


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(length=99), nullable=False)
    second_name: Mapped[str] = mapped_column(String(99), nullable=False)
    phone: Mapped[int | None] = mapped_column(nullable=False)  # необязательное поле [int | None]
    username: Mapped[str] = mapped_column(String(99), nullable=False, unique=True)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    role_id: Mapped[int] = mapped_column(ForeignKey("role_table.id"))

    # из класса просто для простоты вынесем сюда
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # back_populates="user - на что ссылаемся, cascade="all" - при удалении польз. удалить все
    role: Mapped["Role"] = relationship(back_populates="user")
    workout: Mapped[list["Workout"]] = relationship(back_populates="user", cascade="all")
    set: Mapped[list["Set"]] = relationship(back_populates="user", cascade="all")
