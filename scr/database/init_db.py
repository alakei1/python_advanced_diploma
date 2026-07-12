"""
Скрипт для инициализации базы данных:
1. Создает все таблицы
2. Заполняет тестовыми данными
"""

import asyncio
import random
import sys
from datetime import datetime, timedelta

from database import AsyncSessionLocal, Base, engine

# Импортируем таблицу связей напрямую, чтобы избежать ленивой загрузки через ORM
from models import Like, Tweet, User

# Добавлены недостающие импорты из SQLAlchemy
from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_tables():
    """Создает все таблицы в базе данных."""
    print("Создание таблиц...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы созданы!")


async def drop_tables():
    """Удаляет все таблицы."""
    print("Удаление таблиц...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("Таблицы удалены!")


async def seed_users(db: AsyncSession) -> list[User]:
    """Создает тестовых пользователей."""
    print("Создание пользователей...")

    users_data = [
        {"name": "Алиса", "api_key": "alice_key_123"},
        {"name": "Боб", "api_key": "bob_key_456"},
        {"name": "Чарли", "api_key": "charlie_key_789"},
        {"name": "Дина", "api_key": "dina_key_101"},
        {"name": "Егор", "api_key": "egor_key_202"},
        {"name": "Женя", "api_key": "zhenya_key_303"},
        {"name": "Зина", "api_key": "zina_key_404"},
    ]

    users = []
    for data in users_data:
        user = User(
            name=data["name"],
            api_key=data["api_key"],
        )
        db.add(user)
        users.append(user)

    # Используем flush вместо commit, чтобы объекты остались в сессии,
    # но база данных уже сгенерировала для них id
    await db.flush()
    print(f"Создано {len(users)} пользователей")
    return users


async def seed_followers(db: AsyncSession, users: list[User]):
    """Создает подписки между пользователями через прямую асинхронную вставку."""
    print("Создание подписок...")

    follow_relations = set()
    for user in users:
        others = [u for u in users if u.id != user.id]
        to_follow = random.sample(others, k=min(random.randint(2, 3), len(others)))
        for follow in to_follow:
            relation = (user.id, follow.id)
            follow_relations.add(relation)

    insert_data = [
        {"follower_id": f_id, "following_id": target_id}
        for f_id, target_id in follow_relations
    ]

    if insert_data:
        # 1. Получаем объект таблицы из метаданных Base
        followers_table = Base.metadata.tables["followers"]

        # 2. Передаем именно ПРАВИЛЬНУЮ переменную followers_table в функцию insert()
        await db.execute(insert(followers_table), insert_data)
        await db.flush()

    print(f"Создано {len(insert_data)} подписок")


async def seed_tweets(db: AsyncSession, users: list[User]) -> list[Tweet]:
    """Создает тестовые твиты."""
    print("Создание твитов...")

    tweet_contents = [
        "Привет, мир! Это мой первый твит!",
        "Сегодня отличная погода!",
        "Изучаю Python и создаю микроблог!",
        "Кофе - это жизнь!",
        "Заканчиваю проект по микроблогам",
        "Код - это поэзия",
        "Учиться, учиться и еще раз учиться!",
        "Сегодня был продуктивный день",
        "Спасибо всем, кто читает мои твиты!",
        "Новый день - новые возможности",
        "Программирование - это искусство",
        "Работаю над своим проектом",
        "Лучший способ предсказать будущее - создать его",
        "Каждый день учу что-то новое",
        "Делюсь мыслями с миром",
    ]

    tweets = []
    for content in tweet_contents:
        author = random.choice(users)
        tweet = Tweet(
            content=content,
            author_id=author.id,
            created_at=datetime.now() - timedelta(days=random.randint(0, 30)),
        )
        db.add(tweet)
        tweets.append(tweet)

    await db.flush()
    print(f"Создано {len(tweets)} твитов")
    return tweets


async def seed_likes(db: AsyncSession, tweets: list[Tweet], users: list[User]):
    """Создает лайки для твитов."""
    print("Создание лайков...")

    like_count = 0
    for tweet in tweets:
        likers = random.sample(users, k=min(random.randint(1, 5), len(users)))
        for user in likers:
            # Проверка существования лайка теперь работает корректно
            # через асинхронный select
            existing = await db.execute(
                select(Like).where(Like.user_id == user.id, Like.tweet_id == tweet.id)
            )
            if not existing.scalar_one_or_none():
                like = Like(
                    user_id=user.id,
                    tweet_id=tweet.id,
                )
                db.add(like)
                like_count += 1

    await db.flush()
    print(f"Создано {like_count} лайков")


async def init_database():
    """Главная функция инициализации базы данных."""
    print("=" * 50)
    print("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
    print("=" * 50)

    # Используем единую транзакцию на весь процесс наполнения
    async with AsyncSessionLocal() as db:
        async with db.begin():
            # Создаем таблицы
            await create_tables()

            # Заполняем данными последовательно
            users = await seed_users(db)
            await seed_followers(db, users)
            tweets = await seed_tweets(db, users)
            await seed_likes(db, tweets, users)

    print("=" * 50)
    print("БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
    print("=" * 50)

    # Выводим статистику
    async with AsyncSessionLocal() as db:
        user_count = await db.scalar(select(func.count()).select_from(User))
        tweet_count = await db.scalar(select(func.count()).select_from(Tweet))
        like_count = await db.scalar(select(func.count()).select_from(Like))

        print(f"Пользователей: {user_count}")
        print(f"Твитов: {tweet_count}")
        print(f"Лайков: {like_count}")


async def clear_database():
    """Очищает базу данных."""
    print("Очистка базы данных...")
    await drop_tables()
    print("База данных очищена!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        asyncio.run(clear_database())
    else:
        asyncio.run(init_database())
