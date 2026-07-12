"""
Модели базы данных.
"""

from scr.database.models.base import BaseModel, TimestampMixin
from scr.database.models.like import Like
from scr.database.models.media import Media
from scr.database.models.tweet import Tweet
from scr.database.models.user import User

__all__ = [
    "BaseModel",
    "TimestampMixin",
    "User",
    "Tweet",
    "Media",
    "Like",
]
