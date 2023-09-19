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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(length=99), nullable=False)
    permissions: Mapped[JSON] = mapped_column(JSON)

    # тут список потому что много пользователей будет
    user: Mapped[list["User"]] = relationship(back_populates="role")


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    second_name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    registered_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow())
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("role_table.id"))

    # из класса просто для простоты вынесем сюда
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    role: Mapped["Role"] = relationship(back_populates="user")
    workout: Mapped[list["Workout"]] = relationship(back_populates="user")
    set: Mapped[list["Set"]] = relationship(back_populates="user")

# class Role(Base):
#     __tablename__ = "role"
#
#     id = Column(Integer, primary_key=True, index=True, unique=True)
#     name = Column(String, nullable=False)
#     permissions = Column(JSON)
#
#     user = relationship("User", back_populates="role")

# class User(SQLAlchemyBaseUserTable[int], Base):
#     __tablename__ = "user"
#
#     id = Column(Integer, primary_key=True, index=True, unique=True)
#     email = Column(String, nullable=False)
#     first_name = Column(String, nullable=False)
#     second_name = Column(String, nullable=False)
#     phone = Column(Integer, nullable=False)
#     username = Column(String, nullable=False)
#     registered_at = Column(TIMESTAMP, default=datetime.utcnow())
#     role_id = Column(Integer, ForeignKey("role.id"))
#
#     # из класса просто для простоты вынесем сюда
#     hashed_password = Column(String(length=1024), nullable=False)
#     is_active = Column(Boolean, default=True, nullable=False)
#     is_superuser = Column(Boolean, default=False, nullable=False)
#     is_verified = Column(Boolean, default=False, nullable=False)
#
#     role = relationship("Role", back_populates="users")
