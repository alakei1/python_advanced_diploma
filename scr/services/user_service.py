"""
Асинхронный сервис для работы с пользователями.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from scr.database.models import User


class UserService:
    """Асинхронный сервис для работы с пользователями."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, user_id: int) -> User | None:
        """Получить пользователя по ID."""
        result = await self.db.execute(
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.followers),
                selectinload(User.following),
                selectinload(User.tweets),
            )
        )
        return result.scalar_one_or_none()

    async def get_user_by_api_key(self, api_key: str) -> User | None:
        """Получить пользователя по API ключу."""
        result = await self.db.execute(select(User).where(User.api_key == api_key))
        return result.scalar_one_or_none()

    async def get_profile(self, user_id: int) -> User | None:
        """Получить профиль пользователя с подписчиками и подписками."""
        result = await self.db.execute(
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.followers),
                selectinload(User.following),
            )
        )
        return result.scalar_one_or_none()

    async def follow_user(self, follower_id: int, following_id: int) -> bool:
        """Подписаться на пользователя."""
        if follower_id == following_id:
            return False

        # Получаем обоих пользователей
        result = await self.db.execute(
            select(User)
            .where(User.id.in_([follower_id, following_id]))
            .options(selectinload(User.following))
        )
        users = result.scalars().all()

        if len(users) != 2:
            return False

        # Добавили проверку id is not None, чтобы Mypy не ругался на сравнение с int
        follower = next(u for u in users if u.id is not None and u.id == follower_id)
        following = next(u for u in users if u.id is not None and u.id == following_id)

        # Благодаря новой модели User, Mypy знает, что follower.following — это список
        if following in follower.following:
            return False

        follower.following.append(following)
        await self.db.commit()
        return True

    async def unfollow_user(self, follower_id: int, following_id: int) -> bool:
        """Отписаться от пользователя."""
        result = await self.db.execute(
            select(User)
            .where(User.id == follower_id)
            .options(selectinload(User.following))
        )
        follower = result.scalar_one_or_none()

        if not follower:
            return False

        # Добавили проверку id is not None для Mypy
        following = next(
            (
                u
                for u in follower.following
                if u.id is not None and u.id == following_id
            ),
            None,
        )
        if not following:
            return False

        follower.following.remove(following)
        await self.db.commit()
        return True
