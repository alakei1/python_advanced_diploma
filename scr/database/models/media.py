"""Модель медиафайла."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scr.database.models.base import BaseModel, TimestampMixin

# Импортируем Tweet только для проверки типов Mypy,
# чтобы избежать циклических импортов в рантайме.
if TYPE_CHECKING:
    from scr.database.models.tweet import Tweet


class Media(BaseModel, TimestampMixin):
    """Модель медиафайла."""

    __tablename__ = "media"

    # Используем mapped_column и строго указываем типы через Mapped
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)

    tweet_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("tweets.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Явно типизируем связь через Mapped["Tweet"]
    tweet: Mapped["Tweet"] = relationship("Tweet", back_populates="media")

    @property
    def url(self) -> str:
        """URL для доступа к файлу."""
        return f"/uploads/{self.file_path}"

    def __repr__(self) -> str:
        obj_id = getattr(self, "id", None)
        return f"<Media(id={obj_id}, filename={self.filename})>"
