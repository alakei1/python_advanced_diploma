from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.dependencies import get_current_user
from scr.database.database import get_db
from scr.database.models.user import User
from scr.schemas.response import BaseResponse
from scr.schemas.tweet import (
    TweetAuthor,
    TweetCreate,
    TweetCreateResponse,
    TweetLike,
    TweetListResponse,
    TweetResponse,
)
from scr.services.tweet_service import TweetService

router = APIRouter(prefix="/api/tweets", tags=["tweets"])


# ============================================ #
# GET ЛЕНТА ТВИТОВ                             #
# ============================================ #
@router.get("", response_model=TweetListResponse)
async def get_feed(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Получает ленту твитов от пользователей, на которых подписан пользователь."""
    service = TweetService(db)
    tweets = await service.get_feed(current_user.id)

    tweet_responses = [
        TweetResponse(
            id=tweet.id,
            content=tweet.content,
            attachments=[media.url for media in tweet.media],
            author=TweetAuthor(
                id=tweet.author.id,
                name=tweet.author.name,
            ),
            likes=[
                TweetLike(
                    user_id=like.user_id,
                    name=like.user.name if like.user else "Unknown",
                )
                for like in tweet.likes
            ],
            created_at=tweet.created_at,
        )
        for tweet in tweets
    ]

    return TweetListResponse(result=True, tweets=tweet_responses)


# ============================================ #
# POST СОЗДАНИЕ ТВИТА                          #
# ============================================ #
@router.post(
    "", response_model=TweetCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_tweet(
    tweet_data: TweetCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Создает новый твит для текущего пользователя."""
    service = TweetService(db)

    tweet_id = await service.create_tweet(
        user_id=current_user.id,
        content=tweet_data.tweet_data,
        media_ids=tweet_data.tweet_media_ids,
    )

    return TweetCreateResponse(result=True, tweet_id=tweet_id)


# ============================================ #
# DELETE УДАЛЕНИЕ ТВИТА                        #
# ============================================ #
@router.delete("/{tweet_id}", response_model=BaseResponse)
async def delete_tweet(
    tweet_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Удаляет твит пользователя.
    Проверяет, что пользователь удаляет свой собственный твит.
    """
    service = TweetService(db)

    # Используем метод get_tweet вместо get_tweet_by_id
    tweet = await service.get_tweet(tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )

    if tweet.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own tweets",
        )

    # Передаем оба параметра: tweet_id и user_id
    success = await service.delete_tweet(tweet_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet not found or already deleted",
        )

    return BaseResponse(result=True)


# ============================================ #
# POST ЛАЙК ТВИТА                             #
# ============================================ #
@router.post("/{tweet_id}/likes", response_model=BaseResponse)
async def like_tweet(
    tweet_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Ставит отметку "Нравится" на твит.
    """
    service = TweetService(db)

    # Используем метод get_tweet вместо get_tweet_by_id
    tweet = await service.get_tweet(tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )

    # Метод like_tweet сам проверяет, есть ли уже лайк
    # и возвращает False если лайк уже существует
    success = await service.like_tweet(current_user.id, tweet_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already liked this tweet",
        )

    return BaseResponse(result=True)


# ============================================ #
# DELETE УБРАТЬ ЛАЙК С ТВИТА                   #
# ============================================ #
@router.delete("/{tweet_id}/likes", response_model=BaseResponse)
async def unlike_tweet(
    tweet_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Убирает отметку "Нравится" с твита.
    """
    service = TweetService(db)

    # Используем метод get_tweet вместо get_tweet_by_id
    tweet = await service.get_tweet(tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )

    # Метод unlike_tweet сам проверяет, есть ли лайк
    # и возвращает False если лайка не было
    success = await service.unlike_tweet(current_user.id, tweet_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You haven't liked this tweet",
        )

    return BaseResponse(result=True)
