"""Тесты для UserService."""

from sqlalchemy.ext.asyncio import AsyncSession

from scr.database.models import User
from scr.services.user_service import UserService


class TestUserService:
    """Тесты для UserService."""

    async def test_get_user(self, db_session: AsyncSession, test_user: User):
        """Тест получения пользователя."""
        service = UserService(db_session)
        assert test_user.id is not None

        user = await service.get_user(test_user.id)

        assert user is not None
        assert user.id == test_user.id
        assert user.name == test_user.name

    async def test_get_user_by_api_key(self, db_session: AsyncSession, test_user: User):
        """Тест поиска пользователя по API ключу."""
        service = UserService(db_session)

        # Принудительно приводим к str, чтобы PyCharm не ругался на типы ORM
        api_key_str = str(test_user.api_key)
        user = await service.get_user_by_api_key(api_key_str)

        assert user is not None
        assert user.id == test_user.id

    async def test_get_profile(self, db_session: AsyncSession, test_user: User):
        """Тест получения профиля."""
        service = UserService(db_session)
        assert test_user.id is not None

        profile = await service.get_profile(test_user.id)

        assert profile is not None
        assert profile.id == test_user.id
        assert hasattr(profile, "followers")
        assert hasattr(profile, "following")

    async def test_follow_user(
        self, db_session: AsyncSession, test_user: User, test_user2: User
    ):
        """Тест подписки на пользователя."""
        service = UserService(db_session)
        assert test_user.id is not None
        assert test_user2.id is not None

        result = await service.follow_user(test_user.id, test_user2.id)

        assert result is True

        user = await service.get_user(test_user.id)
        assert user is not None
        assert test_user2.id in [u.id for u in user.following]

    async def test_follow_self(self, db_session: AsyncSession, test_user: User):
        """Тест подписки на самого себя."""
        service = UserService(db_session)
        assert test_user.id is not None

        result = await service.follow_user(test_user.id, test_user.id)

        assert result is False

    async def test_unfollow_user(
        self, db_session: AsyncSession, test_user: User, test_user2: User
    ):
        """Тест отписки от пользователя."""
        service = UserService(db_session)
        assert test_user.id is not None
        assert test_user2.id is not None

        await service.follow_user(test_user.id, test_user2.id)
        result = await service.unfollow_user(test_user.id, test_user2.id)

        assert result is True

        user = await service.get_user(test_user.id)
        assert user is not None
        assert test_user2.id not in [u.id for u in user.following]

        user = await service.get_user(test_user.id)
        assert user is not None
        assert test_user2.id not in [u.id for u in user.following]
