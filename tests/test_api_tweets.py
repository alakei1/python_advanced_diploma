"""Тесты для API эндпоинтов твитов."""

import pytest

from scr.database.models import Tweet


@pytest.mark.asyncio
class TestTweetsAPI:
    """Тесты для эндпоинтов твитов (/api/tweets)."""

    async def test_get_feed_empty(self, auth_client, db_session, test_user):
        """Тест получения пустой ленты."""
        response = await auth_client.get("/api/tweets")

        assert response.status_code == 200
        data = response.json()
        assert data["result"] is True
        assert data["tweets"] == []

    async def test_get_feed_with_tweets(self, auth_client, db_session, test_user):
        """Тест получения ленты с твитами."""
        tweet = Tweet(
            content="Test tweet for feed",
            author_id=test_user.id,
        )
        db_session.add(tweet)
        await db_session.commit()

        response = await auth_client.get("/api/tweets")

        assert response.status_code == 200
        data = response.json()
        assert data["result"] is True
        assert len(data["tweets"]) == 1
        assert data["tweets"][0]["content"] == "Test tweet for feed"
        assert data["tweets"][0]["author"]["id"] == test_user.id

    async def test_create_tweet(self, auth_client, db_session, test_user):
        """Тест создания твита."""
        tweet_data = {"tweet_data": "Hello, world!", "tweet_media_ids": []}

        response = await auth_client.post("/api/tweets", json=tweet_data)

        assert response.status_code == 201
        data = response.json()
        assert data["result"] is True
        assert data["tweet_id"] is not None

        tweet = await db_session.get(Tweet, data["tweet_id"])
        assert tweet is not None
        assert tweet.content == "Hello, world!"
        assert tweet.author_id == test_user.id

    async def test_create_tweet_empty_content(self, auth_client, db_session, test_user):
        """Тест создания твита с пустым содержимым."""
        tweet_data = {"tweet_data": "", "tweet_media_ids": []}

        response = await auth_client.post("/api/tweets", json=tweet_data)

        assert response.status_code == 400
        data = response.json()
        assert data["result"] is False
        assert data["error_message"] == "Tweet content cannot be empty"

    async def test_create_tweet_too_long(self, auth_client, db_session, test_user):
        """Тест создания твита длиннее 280 символов."""
        tweet_data = {"tweet_data": "a" * 281, "tweet_media_ids": []}

        response = await auth_client.post("/api/tweets", json=tweet_data)

        assert response.status_code == 400
        data = response.json()
        assert data["result"] is False
        assert data["error_message"] == "Tweet content cannot exceed 280 characters"

    async def test_delete_tweet(self, auth_client, db_session, test_user, test_tweet):
        """Тест удаления твита."""
        response = await auth_client.delete(f"/api/tweets/{test_tweet.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["result"] is True

        deleted = await db_session.get(Tweet, test_tweet.id)
        assert deleted is None

    async def test_delete_tweet_not_found(self, auth_client, db_session, test_user):
        """Тест удаления несуществующего твита."""
        response = await auth_client.delete("/api/tweets/999")

        assert response.status_code == 404
        data = response.json()
        assert data["result"] is False
        assert data["error_message"] == "Tweet not found"

    async def test_delete_tweet_other_user(
        self, auth_client, db_session, test_user, test_user2
    ):
        """Тест удаления твита другого пользователя."""
        tweet = Tweet(
            content="Tweet from other user",
            author_id=test_user2.id,
        )
        db_session.add(tweet)
        await db_session.commit()

        response = await auth_client.delete(f"/api/tweets/{tweet.id}")

        assert response.status_code == 403
        data = response.json()
        assert data["result"] is False
        assert data["error_message"] == "You can only delete your own tweets"

    async def test_like_tweet(self, auth_client, db_session, test_user, test_tweet):
        """Тест лайка твита."""
        response = await auth_client.post(f"/api/tweets/{test_tweet.id}/likes")

        assert response.status_code == 200
        data = response.json()
        assert data["result"] is True

    async def test_like_tweet_already_liked(
        self, auth_client, db_session, test_user, test_tweet
    ):
        """Тест повторного лайка твита."""
        await auth_client.post(f"/api/tweets/{test_tweet.id}/likes")

        response = await auth_client.post(f"/api/tweets/{test_tweet.id}/likes")
        assert response.status_code == 400
        data = response.json()
        assert data["result"] is False
        assert data["error_message"] == "You already liked this tweet"

    async def test_unlike_tweet(self, auth_client, db_session, test_user, test_tweet):
        """Тест удаления лайка."""
        await auth_client.post(f"/api/tweets/{test_tweet.id}/likes")

        response = await auth_client.delete(f"/api/tweets/{test_tweet.id}/likes")
        assert response.status_code == 200
        data = response.json()
        assert data["result"] is True

    async def test_unlike_tweet_not_liked(
        self, auth_client, db_session, test_user, test_tweet
    ):
        """Тест удаления лайка, которого не было."""
        response = await auth_client.delete(f"/api/tweets/{test_tweet.id}/likes")

        assert response.status_code == 400
        data = response.json()
        assert data["result"] is False
        assert data["error_message"] == "You haven't liked this tweet"
