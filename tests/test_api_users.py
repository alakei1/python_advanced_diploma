"""Тесты для API эндпоинтов пользователей."""

import pytest
from sqlalchemy import select

from scr.database.models import User


@pytest.mark.asyncio
class TestUsersAPI:
    """Тесты для эндпоинтов пользователей (/api/users)."""

    async def test_get_my_profile(self, auth_client, db_session, test_user):
        """Тест получения своего профиля."""
        response = await auth_client.get("/api/users/me")

        assert response.status_code == 200
        data = response.json()
        assert data["result"] is True
        assert data["user"]["id"] == test_user.id
        assert data["user"]["name"] == test_user.name

    async def test_get_user_profile(
        self, auth_client, db_session, test_user, test_user2
    ):
        """Тест получения профиля другого пользователя."""
        response = await auth_client.get(f"/api/users/{test_user2.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["result"] is True
        assert data["user"]["id"] == test_user2.id
        assert data["user"]["name"] == test_user2.name

    async def test_get_user_not_found(self, auth_client, db_session, test_user):
        """Тест получения несуществующего пользователя."""
        response = await auth_client.get("/api/users/999")

        assert response.status_code == 404
        data = response.json()
        assert data["result"] is False
        assert data["error_message"] == "User not found"

    async def test_follow_user(self, auth_client, db_session, test_user, test_user2):
        """Тест подписки на пользователя."""
        response = await auth_client.post(f"/api/users/{test_user2.id}/follow")

        assert response.status_code == 200
        data = response.json()
        assert data["result"] is True

        # Проверяем подписку через SQL запрос вместо lazy loading
        result = await db_session.execute(select(User).where(User.id == test_user.id))
        user = result.scalar_one()
        # Принудительно загружаем following
        await db_session.refresh(user, attribute_names=["following"])
        assert test_user2 in user.following

    async def test_follow_self(self, auth_client, db_session, test_user):
        """Тест подписки на самого себя."""
        response = await auth_client.post(f"/api/users/{test_user.id}/follow")

        assert response.status_code == 400
        data = response.json()
        assert data["result"] is False
        assert data["error_message"] == "You cannot follow yourself"

    async def test_follow_already_following(
        self, auth_client, db_session, test_user, test_user2
    ):
        """Тест повторной подписки."""
        await auth_client.post(f"/api/users/{test_user2.id}/follow")

        response = await auth_client.post(f"/api/users/{test_user2.id}/follow")
        assert response.status_code == 400
        data = response.json()
        assert data["result"] is False
        assert data["error_message"] == "Already following this user or user not found"

    async def test_unfollow_user(self, auth_client, db_session, test_user, test_user2):
        """Тест отписки от пользователя."""
        await auth_client.post(f"/api/users/{test_user2.id}/follow")

        response = await auth_client.delete(f"/api/users/{test_user2.id}/follow")
        assert response.status_code == 200
        data = response.json()
        assert data["result"] is True

        # Проверяем отписку через SQL запрос
        result = await db_session.execute(select(User).where(User.id == test_user.id))
        user = result.scalar_one()
        await db_session.refresh(user, attribute_names=["following"])
        assert test_user2 not in user.following

    async def test_unfollow_not_following(
        self, auth_client, db_session, test_user, test_user2
    ):
        """Тест отписки от пользователя, на которого не подписан."""
        response = await auth_client.delete(f"/api/users/{test_user2.id}/follow")

        assert response.status_code == 400
        data = response.json()
        assert data["result"] is False
        assert data["error_message"] == "Not following this user or user not found"
