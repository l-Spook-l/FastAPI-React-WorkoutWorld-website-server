# Это как сериализаторы и валидаторы
from datetime import datetime

from pydantic import BaseModel, Field


class WorkoutCreate(BaseModel):
    name: str
    user_id: int
    description: str
    difficulty: str
    total_time: str


class ExerciseCreate(BaseModel):
    workout_id: int
    description: str
    number_of_sets: int
    maximum_repetitions: int
    rest_time: str
    video: str
    photo: str


class SetCreate(BaseModel):
    exercise_id: int
    user_id: int
    count: int
    weight: int = Field(ge=0)  # число должно быть >= 0


class SetUpdate(BaseModel):
    count: int
