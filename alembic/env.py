import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, async_engine_from_config

from alembic import context

# Импорт настроек и моделей
from config.config import setting_data
from scr.database.database import Base

# Это объект конфигурации Alembic, который предоставляет доступ
# к настройкам в файле .ini.
config = context.config

# Интерпретируем файл конфигурации логирования.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей для autogenerate
target_metadata = Base.metadata


def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме."""
    configuration = config.get_section(config.config_ini_section, {})  # type: ignore

    # Сначала ищем переменную DATABASE_URL от Docker, если её нет - берем из config.py
    database_url: str = os.environ.get("DATABASE_URL", setting_data.database_url)  # type: ignore
    configuration["sqlalchemy.url"] = database_url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Для асинхронного движка используем специальную функцию
    if isinstance(connectable, AsyncEngine):
        # Запускаем асинхронные миграции
        asyncio.run(run_async_migrations(connectable))
    else:
        # Синхронное выполнение (на случай, если движок не асинхронный)
        with connectable.connect() as connection:  # type: ignore[attr-defined]
            context.configure(connection=connection, target_metadata=target_metadata)
            with context.begin_transaction():
                context.run_migrations()


async def run_async_migrations(connectable: AsyncEngine) -> None:
    """Асинхронное выполнение миграций."""
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection) -> None:
    """Фактическое применение миграций."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме."""
    database_url: str = os.environ.get("DATABASE_URL", setting_data.database_url)  # type: ignore
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
