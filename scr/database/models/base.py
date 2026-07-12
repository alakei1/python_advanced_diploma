"""
Базовые классы для моделей.
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from scr.database.database import Base


class BaseModel(Base):
    """Базовый класс с id."""

    __abstract__ = True

    # Используем Mapped вместо Column для поддержки Mypy
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


class TimestampMixin:
    """Миксин с временными метками."""

    # Строго типизируем временные метки через Mapped
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )


__all__ = ["BaseModel", "TimestampMixin"]
