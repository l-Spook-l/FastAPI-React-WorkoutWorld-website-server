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
    name: str
    workout_id: int
    description: str
    number_of_sets: int
    maximum_repetitions: int
    rest_time: int
    video: str
    photo: str


class SetCreate(BaseModel):
    exercise_id: int
    user_id: int
    count: int
    weight: int = Field(ge=0)  # число должно быть >= 0


class WorkoutUpdate(BaseModel):
    name: str = None
    description: str = None
    difficulty: str = None
    total_time: str = None


class ExerciseUpdate(BaseModel):
    name: str = None
    description: str = None
    number_of_sets: int = None
    maximum_repetitions: int = None
    rest_time: int = None
    video: str = None
    photo: str = None


class SetUpdate(BaseModel):
    count: int = None
    weight: int = None
