"""
Схемы для работы с медиафайлами.
"""

from pydantic import BaseModel


class MediaBase(BaseModel):
    """Базовая схема медиафайла."""

    id: int
    filename: str
    url: str
    tweet_id: int | None = None


class MediaCreate(BaseModel):
    """Схема для создания медиафайла."""

    filename: str
    tweet_id: int | None = None


class MediaResponse(BaseModel):
    """Ответ с информацией о медиафайле."""

    result: bool = True
    media_id: int
    url: str
