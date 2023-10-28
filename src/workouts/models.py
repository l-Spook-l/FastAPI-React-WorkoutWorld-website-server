# Ну это модели
from __future__ import annotations  # делает ненужным импорт моделей

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, TIMESTAMP, Boolean, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base

# from src.auth.models import User

# added_workouts_association.c.user_table - доступ к полю
added_workouts_association = Table(
    "added_workouts_association",
    Base.metadata,
    Column("workout_table", ForeignKey("workout_table.id")),
    Column("user_table", ForeignKey("user_table.id")),
)

# photo_for_exercise = Table(
#     "photos_for_exercise",
#     Base.metadata,
#     Column("exercise_photo_table", ForeignKey("exercise_photo_table.id")),
#     Column("exercise_table", ForeignKey("exercise_table.id")),
# )


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
    exercise: Mapped[list["Exercise"]] = relationship(back_populates="workout", cascade="all, delete-orphan", order_by="Exercise.id")


class Exercise(Base):
    __tablename__ = "exercise_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(length=256))
    workout_id: Mapped[int] = mapped_column(ForeignKey("workout_table.id", ondelete="CASCADE"))
    description: Mapped[str] = mapped_column(String(length=500))
    number_of_sets: Mapped[int]
    maximum_repetitions: Mapped[int]
    rest_time: Mapped[int | None]
    video: Mapped[str | None]

    workout: Mapped["Workout"] = relationship(back_populates="exercise")
    set: Mapped[list["Set"]] = relationship(back_populates="exercise", cascade="all, delete-orphan")
    photo: Mapped[list["Exercise_photo"]] = relationship(back_populates="exercise_photo", cascade="all, delete-orphan")


class Set(Base):
    __tablename__ = "set_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise_table.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    repetition: Mapped[int]
    weight: Mapped[int]

    exercise: Mapped["Exercise"] = relationship(back_populates="set")
    user: Mapped["User"] = relationship(back_populates="set")


class Exercise_photo(Base):  # и из папки тоже удалять при удалении
    __tablename__ = "exercise_photo_table"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise_table.id", ondelete="CASCADE"))
    photo: Mapped[str | None]
