"""
Схемы для работы с твитами.
"""

from datetime import datetime

from pydantic import BaseModel


class TweetAuthor(BaseModel):
    """Автор твита (сокращенная версия)."""

    id: int
    name: str


class TweetLike(BaseModel):
    """Лайк на твите."""

    user_id: int
    name: str


class TweetResponse(BaseModel):
    """Полная информация о твите."""

    id: int
    content: str
    attachments: list[str] = []
    author: TweetAuthor
    likes: list[TweetLike] = []
    created_at: datetime


class TweetCreate(BaseModel):
    """Схема для создания твита."""

    tweet_data: str
    tweet_media_ids: list[int] | None = None


class TweetListResponse(BaseModel):
    """Ответ со списком твитов."""

    result: bool = True
    tweets: list[TweetResponse] = []


class TweetDeleteResponse(BaseModel):
    """Ответ на удаление твита."""

    result: bool = True
    message: str = "Tweet deleted successfully"


class TweetCreateResponse(BaseModel):
    """
    Схема ответа при создании нового твита.

    Attributes:
        result (bool): Статус операции (всегда True при успехе)
        tweet_id (int): ID созданного твита
    """

    result: bool
    tweet_id: int

    class Config:
        json_schema_extra = {"example": {"result": True, "tweet_id": 42}}
