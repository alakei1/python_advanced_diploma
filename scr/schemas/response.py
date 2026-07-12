"""
Базовые схемы для ответов API.
"""

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """Базовый ответ API."""

    result: bool = True
    tweet_id: int | None = None


class MediaUploadResponse(BaseModel):
    """Ответ на загрузку медиафайла."""

    result: bool = True
    media_id: int


class ErrorResponse(BaseModel):
    """Ответ при ошибке."""

    result: bool = False
    error_type: str
    error_message: str
