"""Тесты для TweetService."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from scr.database.models import Like, Tweet, User
from scr.services.tweet_service import TweetService


class TestTweetService:
    """Тесты для TweetService."""

    async def test_create_tweet(self, db_session: AsyncSession, test_user: User):
        """Тест создания твита."""
        service = TweetService(db_session)
        assert test_user.id is not None

        tweet_id = await service.create_tweet(
            user_id=test_user.id, content="Test tweet"
        )

        assert tweet_id is not None
        assert isinstance(tweet_id, int)

        # Проверяем, что твит сохранился
        tweet = await service.get_tweet(tweet_id)
        assert tweet is not None
        assert tweet.content == "Test tweet"
        assert tweet.author_id == test_user.id

    async def test_get_tweet(self, db_session: AsyncSession, test_tweet: Tweet):
        """Тест получения твита по ID."""
        service = TweetService(db_session)
        assert test_tweet.id is not None

        tweet = await service.get_tweet(test_tweet.id)

        assert tweet is not None
        assert tweet.id == test_tweet.id
        assert tweet.content == test_tweet.content

    async def test_get_tweet_not_found(self, db_session: AsyncSession):
        """Тест получения несуществующего твита."""
        service = TweetService(db_session)

        tweet = await service.get_tweet(999)

        assert tweet is None

    async def test_delete_tweet(self, db_session: AsyncSession, test_tweet: Tweet):
        """Тест удаления твита."""
        service = TweetService(db_session)
        assert test_tweet.id is not None
        assert test_tweet.author_id is not None

        result = await service.delete_tweet(
            tweet_id=test_tweet.id, user_id=test_tweet.author_id
        )

        assert result is True

        deleted = await service.get_tweet(test_tweet.id)
        assert deleted is None

    async def test_delete_tweet_wrong_user(
        self, db_session: AsyncSession, test_tweet: Tweet
    ):
        """Тест удаления твита чужим пользователем."""
        service = TweetService(db_session)
        assert test_tweet.id is not None

        result = await service.delete_tweet(tweet_id=test_tweet.id, user_id=999)

        assert result is False

    async def test_like_tweet(
        self, db_session: AsyncSession, test_tweet: Tweet, test_user: User
    ):
        """Тест лайка твита."""
        service = TweetService(db_session)
        assert test_user.id is not None
        assert test_tweet.id is not None

        result = await service.like_tweet(user_id=test_user.id, tweet_id=test_tweet.id)

        assert result is True

        like_count = await db_session.scalar(
            select(func.count()).select_from(Like).where(Like.tweet_id == test_tweet.id)
        )
        assert like_count == 1

    async def test_like_tweet_already_liked(
        self, db_session: AsyncSession, test_tweet: Tweet, test_user: User
    ):
        """Тест повторного лайка твита."""
        service = TweetService(db_session)
        assert test_user.id is not None
        assert test_tweet.id is not None

        await service.like_tweet(test_user.id, test_tweet.id)
        result = await service.like_tweet(test_user.id, test_tweet.id)

        assert result is False

    async def test_unlike_tweet(
        self, db_session: AsyncSession, test_tweet: Tweet, test_user: User
    ):
        """Тест удаления лайка."""
        service = TweetService(db_session)
        assert test_user.id is not None
        assert test_tweet.id is not None

        await service.like_tweet(test_user.id, test_tweet.id)
        result = await service.unlike_tweet(test_user.id, test_tweet.id)

        assert result is True

        like_count = await db_session.scalar(
            select(func.count()).select_from(Like).where(Like.tweet_id == test_tweet.id)
        )
        assert like_count == 0

    async def test_unlike_tweet_not_liked(
        self, db_session: AsyncSession, test_tweet: Tweet, test_user: User
    ):
        """Тест удаления лайка, которого не было."""
        service = TweetService(db_session)
        assert test_user.id is not None
        assert test_tweet.id is not None

        # Пытаемся убрать лайк, не лайкая твит заранее
        result = await service.unlike_tweet(test_user.id, test_tweet.id)

        assert result is False  # Сервис должен вернуть False, так как лайка нет
