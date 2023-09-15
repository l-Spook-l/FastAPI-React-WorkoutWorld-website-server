# Ну это модели
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from fastapi_users.db import SQLAlchemyBaseUserTable

from src.database import Base


class Workout(Base):
    __tablename__ = "workout"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    user_id = Column(JSON)
    description = Column(String(length=1000))
    created_at = Column(TIMESTAMP, default=datetime.utcnow())
    difficulty = Column(String)
    timer = Column(DateTime)


class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    workout_id = Column()
    description = Column(String(length=500))
    number_of_sets = Column(Integer)
    maximum_repetitions = Column(Integer)
    rest_time = Column()
    weight = Column(Integer)
    timer = Column()


class Set(Base):
    __tablename__ = "set"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    exercises_id = Column()
    user_id = Column()
    count = Column(Integer)

    # id = Column(Integer, primary_key=True, index=True, unique=True)
    # email = Column(String, nullable=False)
    # first_name = Column(String, nullable=False)
    # second_name = Column(String, nullable=False)
    # phone = Column(Integer, nullable=False)
    # username = Column(String, nullable=False)
    # registered_at = Column(TIMESTAMP, default=datetime.utcnow())
    # role_id = Column(Integer, ForeignKey("role.id"))
    #
    # # из класса просто для простоты вынесем сюда
    # hashed_password = Column(String(length=1024), nullable=False)
    # is_active = Column(Boolean, default=True, nullable=False)
    # is_superuser = Column(Boolean, default=False, nullable=False)
    # is_verified = Column(Boolean, default=False, nullable=False)
    #
    # role = relationship(Role)
