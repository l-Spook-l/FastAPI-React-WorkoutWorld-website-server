from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base

from .config import DB_NAME, DB_PORT, DB_HOST, DB_PASSWORD, DB_USER

# DATABASE_URL = "sqlite+aiosqlite:///./test.db"
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Это 2 разных способа
# Base = declarative_base()
class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)  # точка входа sqlalchemy в наше приложение (движок)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)  # переменная для асинхронных сессий


# получение сессий
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
