"""
Схемы для работы с пользователями.
"""

from pydantic import BaseModel


class UserBase(BaseModel):
    """Базовая схема пользователя."""

    id: int
    name: str


class UserProfile(BaseModel):
    """Профиль пользователя с подписчиками и подписками."""

    id: int
    name: str
    followers: list[UserBase] = []
    following: list[UserBase] = []


class UserProfileResponse(BaseModel):
    """Ответ с профилем пользователя."""

    result: bool = True
    user: UserProfile


class UserAuthResponse(BaseModel):
    """Ответ с данными аутентификации."""

    id: int
    name: str
    api_key: str
