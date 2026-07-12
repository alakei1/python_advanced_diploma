"""
Модель пользователя.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scr.database.database import Base
from scr.database.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from scr.database.models.like import Like
    from scr.database.models.tweet import Tweet

# Ассоциативная таблица для подписок
followers = Table(
    "followers",
    Base.metadata,
    Column(
        "follower_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "following_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    extend_existing=True,
)


class User(BaseModel, TimestampMixin):
    """Модель пользователя."""

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    api_key: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    # Связи (relationships) обязательно должны иметь аннотацию Mapped[...]
    tweets: Mapped[list["Tweet"]] = relationship(
        "Tweet", back_populates="author", cascade="all, delete-orphan"
    )
    likes: Mapped[list["Like"]] = relationship(
        "Like", back_populates="user", cascade="all, delete-orphan"
    )

    # На кого подписан текущий пользователь (возвращает список объектов User)
    following: Mapped[list["User"]] = relationship(
        "User",
        secondary=followers,
        primaryjoin="User.id == followers.c.follower_id",
        secondaryjoin="User.id == followers.c.following_id",
        back_populates="followers",
    )

    # Кто подписан на текущего пользователя
    followers: Mapped[list["User"]] = relationship(
        "User",
        secondary=followers,
        primaryjoin="User.id == followers.c.following_id",
        secondaryjoin="User.id == followers.c.follower_id",
        back_populates="following",
    )

    def __repr__(self) -> str:
        obj_id = getattr(self, "id", None)
        return f"<User(id={obj_id}, name={self.name})>"
