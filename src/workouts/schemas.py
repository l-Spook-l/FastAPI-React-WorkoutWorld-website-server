# Это как сериализаторы и валидаторы
from pydantic import BaseModel, Field
from typing import Optional


class WorkoutCreate(BaseModel):
    name: str
    user_id: int
    description: str
    is_public: bool
    difficulty: str
    total_time: str  # для дальнейшей разработки


class ExerciseCreate(BaseModel):
    name: str
    workout_id: int
    description: str
    number_of_sets: int
    maximum_repetitions: int
    rest_time: int
    video: Optional[str | None]


class SetCreate(BaseModel):
    exercise_id: int
    user_id: int
    repetition: int
    weight: int = Field(ge=0)  # число должно быть >= 0


class WorkoutUpdate(BaseModel):
    name: str = None
    description: str = None
    is_public: bool = None
    difficulty: str = None
    total_time: str = None


class ExerciseUpdate(BaseModel):
    name: str = None
    description: str = None
    number_of_sets: int = None
    maximum_repetitions: int = None
    rest_time: int = None
    video: str = None


class SetUpdate(BaseModel):
    repetition: int = None
    weight: int = None
