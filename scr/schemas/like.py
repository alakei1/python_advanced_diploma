"""
Схемы для работы с лайками.
"""

from pydantic import BaseModel


class LikeResponse(BaseModel):
    """Ответ на действие с лайком."""

    result: bool = True
    message: str = "Like toggled successfully"
