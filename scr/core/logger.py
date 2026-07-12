import sys
from pathlib import Path
from typing import Any, cast

from aiologger import Logger
from aiologger.formatters.base import Formatter
from aiologger.handlers.files import AsyncFileHandler
from aiologger.handlers.streams import AsyncStreamHandler
from aiologger.levels import LogLevel

# ============================================ #
# НАСТРОЙКИ ЛОГГЕРА (все здесь)                #
# ============================================ #
LOG_DIR = "./logs"  # Папка для логов (строка в кавычках)
LOG_LEVEL = "DEBUG"  # Уровень: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "[%(asctime)s] %(filename)s:%(lineno)d [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================ #


class AppLogger:
    """Централизованный логгер для приложения."""

    _instance: Logger | None = None

    @classmethod
    def get_logger(cls, name: str = "microblog") -> Logger:
        """Получить или создать экземпляр логгер-синглтона."""
        if cls._instance is None:
            cls._instance = cls._create_logger(name)

        return cast(Logger, cls._instance)

    @classmethod
    def _create_logger(cls, name: str) -> Logger:
        """Создать и настроить логгер."""
        level_str = LOG_LEVEL.upper()
        log_level = getattr(LogLevel, level_str, LogLevel.DEBUG)

        logger_instance = Logger(name=name, level=log_level)
        formatter = Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

        # Консольный обработчик
        console_handler = AsyncStreamHandler(
            stream=sys.stdout,
            formatter=formatter,
            level=log_level,
        )
        logger_instance.add_handler(console_handler)

        # Создаем папку для логов, если её нет
        log_dir = Path(LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Файловый обработчик (все логи) - БЕЗ лишних аргументов в __init__
        file_handler = AsyncFileHandler(
            filename=str(log_dir / "app.log"), mode="a", encoding="utf-8"
        )
        # Настройка через атрибуты напрямую
        file_handler.formatter = formatter
        file_handler.level = log_level
        logger_instance.add_handler(file_handler)

        # Отдельный файл для ошибок (только ERROR и выше)
        error_handler = AsyncFileHandler(
            filename=str(log_dir / "errors.log"), mode="a", encoding="utf-8"
        )
        # Настройка через атрибуты напрямую
        error_handler.formatter = formatter
        error_handler.level = LogLevel.ERROR
        logger_instance.add_handler(error_handler)

        return logger_instance

    @classmethod
    async def shutdown(cls) -> None:
        """Закрыть логгер и дождаться записи всех сообщений в буфере."""
        if cls._instance:
            await cls._instance.shutdown()
            cls._instance = None


# ============================================ #
# ГЛОБАЛЬНЫЙ ЛОГГЕР И ФУНКЦИИ-ОБЕРТКИ          #
# ============================================ #
logger: Logger = AppLogger.get_logger()


async def log_info(message: str, **kwargs: Any) -> None:
    """Логирование информационного сообщения."""
    await logger.info(message, extra=kwargs if kwargs else None)


async def log_error(message: str, **kwargs: Any) -> None:
    """Логирование сообщения об ошибке."""
    await logger.error(message, extra=kwargs if kwargs else None)


async def log_debug(message: str, **kwargs: Any) -> None:
    """Логирование отладочного сообщения."""
    await logger.debug(message, extra=kwargs if kwargs else None)


async def log_warning(message: str, **kwargs: Any) -> None:
    """Логирование предупреждения."""
    await logger.warning(message, extra=kwargs if kwargs else None)


__all__ = [
    "AppLogger",
    "logger",
    "log_info",
    "log_error",
    "log_debug",
    "log_warning",
]
