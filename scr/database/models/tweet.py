"""Модель твита."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scr.database.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from scr.database.models.like import Like
    from scr.database.models.media import Media
    from scr.database.models.user import User


class Tweet(BaseModel, TimestampMixin):
    """Модель твита."""

    __tablename__ = "tweets"

    content: Mapped[str] = mapped_column(String(280), nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Используем встроенный тип list вместо устаревшего List
    author: Mapped["User"] = relationship("User", back_populates="tweets")
    likes: Mapped[list["Like"]] = relationship(
        "Like", back_populates="tweet", cascade="all, delete-orphan"
    )
    media: Mapped[list["Media"]] = relationship(
        "Media", back_populates="tweet", cascade="all, delete-orphan"
    )

    @property
    def likes_count(self) -> int:
        """Количество лайков твита."""
        # Явно получаем коллекцию как список, обходя ложное предупреждение PyCharm
        likes_list = getattr(self, "likes", [])
        return len(likes_list) if likes_list is not None else 0

    def __repr__(self) -> str:
        obj_id = getattr(self, "id", None)
        return f"<Tweet(id={obj_id}, author_id={self.author_id})>"
