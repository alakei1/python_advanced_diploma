"""Фикстуры для тестов."""

import logging
import os
import sys
from unittest.mock import MagicMock

import pytest
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

# ОТКЛЮЧАЕМ ЛОГГИРОВАНИЕ
logging.disable(logging.CRITICAL)


# МОКАЕМ ЛОГГЕР
class AsyncMockLogger:
    async def info(self, message, *args, **kwargs):
        pass

    async def error(self, message, *args, **kwargs):
        pass

    async def debug(self, message, *args, **kwargs):
        pass

    async def warning(self, message, *args, **kwargs):
        pass

    async def critical(self, message, *args, **kwargs):
        pass


mock_logger = AsyncMockLogger()
# Создаём мок-объект для модуля с нужными атрибутами
mock_logger_module = MagicMock()
mock_logger_module.logger = mock_logger
mock_logger_module.log_info = mock_logger.info
mock_logger_module.log_error = mock_logger.error
mock_logger_module.log_debug = mock_logger.debug
mock_logger_module.log_warning = mock_logger.warning
mock_logger_module.log_critical = mock_logger.critical

sys.modules["scr.core.logger"] = mock_logger_module

# Теперь импортируем всё остальное
from scr.app.main import app  # noqa: E402
from scr.database.database import Base, get_db  # noqa: E402
from scr.database.models import Tweet, User  # noqa: E402


class MockSettings:
    database_url = "postgresql+asyncpg://admin:admin@localhost:5432/postgres"


# Мокаем config
mock_config = MagicMock()
mock_config.setting_data = MockSettings()
sys.modules["config"] = mock_config
sys.modules["config.config"] = mock_config


def get_test_database_url():
    """Возвращает URL для тестовой БД."""
    is_ci = os.getenv("CI", "false").lower() == "true"
    is_gitlab = os.getenv("GITLAB_CI", "false").lower() == "true"

    if is_ci or is_gitlab:
        return "postgresql+asyncpg://postgres:postgres@postgres:5432/twitter_test"

    return "postgresql+asyncpg://admin:admin@localhost:5432/postgre"


TEST_DATABASE_URL = get_test_database_url()

# АСИНХРОННЫЙ engine
engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)
TestingAsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def run_sync_create_all(conn: Connection) -> None:
    Base.metadata.create_all(conn)


def run_sync_drop_all(conn: Connection) -> None:
    Base.metadata.drop_all(conn)


@pytest.fixture(scope="function")
async def db_session():
    """Асинхронная фикстура для БД."""
    async with engine.begin() as conn:
        await conn.run_sync(run_sync_drop_all)
        await conn.run_sync(run_sync_create_all)

    async with TestingAsyncSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(run_sync_drop_all)


@pytest.fixture(scope="function")
async def test_user(db_session):
    """Фикстура тестового пользователя."""
    user = User(
        name="Test User",
        api_key="test_key_123",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def test_user2(db_session):
    """Фикстура второго пользователя."""
    user = User(
        name="Test User 2",
        api_key="test_key_456",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def test_tweet(db_session, test_user):
    """Фикстура тестового твита."""
    tweet = Tweet(
        content="Test tweet content",
        author_id=test_user.id,
    )
    db_session.add(tweet)
    await db_session.commit()
    await db_session.refresh(tweet)
    return tweet


# АСИНХРОННЫЙ КЛИЕНТ
@pytest.fixture(scope="function")
async def auth_client(db_session, test_user):
    """Асинхронный клиент с авторизацией."""
    from httpx import ASGITransport, AsyncClient

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        client.headers.update({"api-key": "test_key_123"})
        yield client

    app.dependency_overrides.clear()
