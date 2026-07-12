"""Асинхронный сервис для работы с твитами."""

from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from scr.database.models import Like as LikeModel
from scr.database.models import Media, Tweet, User


class TweetService:
    """Асинхронный сервис для работы с твитами."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_tweet(
        self,
        user_id: int,
        content: str,
        media_ids: list[int] | None = None,
    ) -> int:
        """
        Создать твит (асинхронно).

        Args:
            user_id: ID автора твита
            content: Текст твита
            media_ids: Список ID медиафайлов (опционально)

        Returns:
            int: ID созданного твита
        """
        # Валидация контента
        if not content or not content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tweet content cannot be empty",
            )

        if len(content) > 280:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tweet content cannot exceed 280 characters",
            )

        # Создаем твит
        tweet = Tweet(
            content=content.strip(),
            author_id=user_id,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(tweet)
        await self.db.flush()

        # Привязываем медиафайлы (без проверки user_id, т.к. в модели его нет)
        if media_ids:
            for media_id in media_ids:
                media = await self.db.get(Media, media_id)
                if not media:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Media {media_id} not found",
                    )

                # Проверяем, не привязано ли медиа к другому твиту
                if media.tweet_id is not None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Media {media_id} is already attached to another tweet",
                    )

                media.tweet_id = tweet.id

        await self.db.commit()
        await self.db.refresh(tweet)
        return tweet.id

    async def get_tweet(self, tweet_id: int) -> Tweet | None:
        """Получить твит по ID (асинхронно)."""
        result = await self.db.execute(
            select(Tweet)
            .where(Tweet.id == tweet_id)
            .options(
                selectinload(Tweet.author),
                selectinload(Tweet.media),
                selectinload(Tweet.likes).selectinload(LikeModel.user),
            )
        )
        return result.scalar_one_or_none()

    async def get_feed(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Tweet]:
        """Получить ленту твитов (асинхронно)."""
        user_result = await self.db.execute(
            select(User).where(User.id == user_id).options(selectinload(User.following))
        )
        user = user_result.scalar_one_or_none()

        if user is None:
            return []

        following_ids = [user_id]

        # Добавляем подписки, если они есть
        if user.following:
            following_ids.extend([u.id for u in user.following])

        following_ids = list(set(following_ids))

        tweets_result = await self.db.execute(
            select(Tweet)
            .where(Tweet.author_id.in_(following_ids))
            .options(
                selectinload(Tweet.author),
                selectinload(Tweet.media),
                selectinload(Tweet.likes).selectinload(LikeModel.user),
            )
            .order_by(Tweet.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(tweets_result.scalars().all())

    async def delete_tweet(self, tweet_id: int, user_id: int) -> bool:
        """Удалить твит (асинхронно)."""
        # Получаем твит с медиа
        tweet = await self.get_tweet(tweet_id)
        if not tweet or tweet.author_id != user_id:
            return False

        from pathlib import Path

        from config.config import settings_log

        for media in tweet.media:
            if media.file_path:
                upload_dir = Path(settings_log.UPLOAD_DIR)
                file_path = upload_dir / media.file_path
                if file_path.exists():
                    try:
                        file_path.unlink()
                    except OSError:
                        pass

        # Удаляем лайки
        await self.db.execute(delete(LikeModel).where(LikeModel.tweet_id == tweet_id))

        # Удаляем твит
        result = await self.db.execute(
            delete(Tweet).where(
                Tweet.id == tweet_id,
                Tweet.author_id == user_id,
            )
        )
        await self.db.commit()

        return result.rowcount > 0 if hasattr(result, "rowcount") else False

    async def like_tweet(self, user_id: int, tweet_id: int) -> bool:
        """Лайкнуть твит (асинхронно)."""
        tweet = await self.db.get(Tweet, tweet_id)
        if not tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
            )

        result = await self.db.execute(
            select(LikeModel).where(
                LikeModel.user_id == user_id,
                LikeModel.tweet_id == tweet_id,
            )
        )
        if result.scalar_one_or_none() is not None:
            return False

        like = LikeModel(
            user_id=user_id, tweet_id=tweet_id, created_at=datetime.now(timezone.utc)
        )
        self.db.add(like)
        await self.db.commit()
        return True

    async def unlike_tweet(self, user_id: int, tweet_id: int) -> bool:
        """Убрать лайк (асинхронно)."""
        tweet = await self.db.get(Tweet, tweet_id)
        if not tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
            )

        result = await self.db.execute(
            delete(LikeModel).where(
                LikeModel.user_id == user_id,
                LikeModel.tweet_id == tweet_id,
            )
        )
        await self.db.commit()

        return result.rowcount > 0 if hasattr(result, "rowcount") else False
