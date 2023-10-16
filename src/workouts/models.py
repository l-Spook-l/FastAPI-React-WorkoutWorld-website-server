# Ну это модели
from __future__ import annotations  # делает ненужным импорт моделей

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, TIMESTAMP, Boolean, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base

# from src.auth.models import User

added_workouts_association = Table(
    "added_workouts_association",
    Base.metadata,
    Column("workout_table", ForeignKey("workout_table.id")),
    Column("user_table", ForeignKey("user_table.id")),
)


class Workout(Base):
    __tablename__ = "workout_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(length=256))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    description: Mapped[str] = mapped_column(String(length=1000))
    is_public: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    difficulty: Mapped[str] = mapped_column(String(length=50))
    total_time: Mapped[str] = mapped_column(String(length=999))

    user: Mapped["User"] = relationship(back_populates="created_workouts")
    exercise: Mapped[list["Exercise"]] = relationship(back_populates="workout", cascade="all", order_by="Exercise.id")


class Exercise(Base):
    __tablename__ = "exercise_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(length=256))
    workout_id: Mapped[int] = mapped_column(ForeignKey("workout_table.id"))
    description: Mapped[str] = mapped_column(String(length=500))
    number_of_sets: Mapped[int]
    maximum_repetitions: Mapped[int]
    rest_time: Mapped[int | None]
    video: Mapped[str | None]
    photo: Mapped[str | None]

    workout: Mapped["Workout"] = relationship(back_populates="exercise")
    set: Mapped[list["Set"]] = relationship(back_populates="exercise")


class Set(Base):
    __tablename__ = "set_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise_table.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    count: Mapped[int]
    weight: Mapped[int]

    exercise: Mapped["Exercise"] = relationship(back_populates="set")
    user: Mapped["User"] = relationship(back_populates="set")
