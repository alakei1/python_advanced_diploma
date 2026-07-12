from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.dependencies import get_current_user
from scr.database.database import get_db
from scr.database.models.user import User
from scr.schemas.response import BaseResponse
from scr.schemas.user import UserBase, UserProfile, UserProfileResponse
from scr.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Получает информацию о профиле текущего пользователя."""
    service = UserService(db)
    user = await service.get_profile(current_user.id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    profile_data = UserProfile(
        id=user.id,
        name=user.name,
        followers=[UserBase(id=f.id, name=f.name) for f in user.followers],
        following=[UserBase(id=f.id, name=f.name) for f in user.following],
    )
    return UserProfileResponse(result=True, user=profile_data)


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Получает информацию о произвольном профиле по его id."""
    service = UserService(db)
    user = await service.get_profile(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    profile_data = UserProfile(
        id=user.id,
        name=user.name,
        followers=[UserBase(id=f.id, name=f.name) for f in user.followers],
        following=[UserBase(id=f.id, name=f.name) for f in user.following],
    )
    return UserProfileResponse(result=True, user=profile_data)


@router.post("/{user_id}/follow", response_model=BaseResponse)
async def follow_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Начинает подписку на другого пользователя."""
    # Проверка на подписку на себя
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself"
        )

    service = UserService(db)
    success = await service.follow_user(current_user.id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already following this user or user not found",
        )

    return BaseResponse(result=True)


@router.delete("/{user_id}/follow", response_model=BaseResponse)
async def unfollow_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Прекращает подписку на другого пользователя."""
    # Проверка на отписку от себя
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot unfollow yourself",
        )

    service = UserService(db)
    success = await service.unfollow_user(current_user.id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not following this user or user not found",
        )

    return BaseResponse(result=True)
