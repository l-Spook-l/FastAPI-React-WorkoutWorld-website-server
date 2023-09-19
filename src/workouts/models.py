# Ну это модели
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
# from src.auth.models import User


class Workout(Base):
    __tablename__ = "workout_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(length=256))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_table.id"))
    description: Mapped[str] = mapped_column(String(length=1000))
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow())
    difficulty: Mapped[str] = mapped_column(String(length=50))
    timer: Mapped[DateTime] = mapped_column(DateTime)

    user: Mapped["User"] = relationship(back_populates="workout")
    exercises: Mapped[list["Exercise"]] = relationship(back_populates="workout")


class Exercise(Base):
    __tablename__ = "exercise_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    workout_id: Mapped[int] = mapped_column(Integer, ForeignKey("workout_table.id"))
    description: Mapped[str] = mapped_column(String(length=500))
    number_of_sets: Mapped[int] = mapped_column(Integer)
    maximum_repetitions: Mapped[int] = mapped_column(Integer)
    rest_time: Mapped[DateTime] = mapped_column(DateTime)
    weight: Mapped[int] = mapped_column(Integer)
    timer: Mapped[DateTime] = mapped_column(DateTime)

    workout: Mapped["Workout"] = relationship(back_populates="exercise")
    set: Mapped[list["Set"]] = relationship(back_populates="exercise")


class Set(Base):
    __tablename__ = "set_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    exercises_id: Mapped[int] = mapped_column(Integer, ForeignKey("exercise_table.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_table.id"))
    count: Mapped[int] = mapped_column(Integer)

    exercises: Mapped["Exercise"] = relationship(back_populates="set")
    user: Mapped["User"] = relationship(back_populates="set")
