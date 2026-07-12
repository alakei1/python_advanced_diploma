"""
Настройка подключения к базе данных
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config.config import setting_data

url: str = setting_data.database_url

engine = create_async_engine(
    url=url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False,
    pool_recycle=3600,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# Создаем декларативную базу в стиле SQLAlchemy 2.0
class Base(DeclarativeBase):
    """Корневой декларативный класс для всех моделей."""

    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для получения асинхронной сессии БД."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
