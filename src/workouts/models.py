# Ну это модели
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
# from src.auth.models import User


class Workout(Base):
    __tablename__ = "workout_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(length=256))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    description: Mapped[str] = mapped_column(String(length=1000))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    difficulty: Mapped[str] = mapped_column(String(length=50))

    user: Mapped["User"] = relationship(back_populates="workout")
    exercise: Mapped[list["Exercise"]] = relationship(back_populates="workout")


class Exercise(Base):
    __tablename__ = "exercise_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey("workout_table.id"))
    description: Mapped[str] = mapped_column(String(length=500))
    number_of_sets: Mapped[int]
    maximum_repetitions: Mapped[int]
    rest_time: Mapped[datetime]
    weight: Mapped[int]
    timer: Mapped[datetime]

    workout: Mapped["Workout"] = relationship(back_populates="exercise")
    set: Mapped[list["Set"]] = relationship(back_populates="exercise")


class Set(Base):
    __tablename__ = "set_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise_table.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    count: Mapped[int]

    exercise: Mapped["Exercise"] = relationship(back_populates="set")
    user: Mapped["User"] = relationship(back_populates="set")
