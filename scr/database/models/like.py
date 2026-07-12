"""Модель лайка."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scr.database.models.base import BaseModel, TimestampMixin

# Импортируем другие модели только для проверки типов Mypy,
# чтобы избежать циклических импортов.
if TYPE_CHECKING:
    from scr.database.models.tweet import Tweet
    from scr.database.models.user import User


class Like(BaseModel, TimestampMixin):
    """Модель лайка."""

    __tablename__ = "likes"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tweet_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tweets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship("User", back_populates="likes", lazy="joined")
    tweet: Mapped["Tweet"] = relationship(
        "Tweet", back_populates="likes", lazy="joined"
    )

    __table_args__ = (
        UniqueConstraint("user_id", "tweet_id", name="unique_user_tweet_like"),
    )

    def __repr__(self) -> str:
        return f"<Like(user_id={self.user_id}, tweet_id={self.tweet_id})>"
