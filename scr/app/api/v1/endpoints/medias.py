from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.dependencies import get_current_user
from scr.database.database import get_db
from scr.database.models.user import User
from scr.schemas.response import MediaUploadResponse
from scr.services.media_service import MediaService

router = APIRouter(prefix="/api/medias", tags=["medias"])


@router.post("", response_model=MediaUploadResponse)
async def upload_media(
    file: Annotated[UploadFile, File(...)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Загружает медиафайл для твита."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image.",
        )

    service = MediaService(db)
    media = await service.save_media(
        file=file,
        user_id=current_user.id,
    )

    return MediaUploadResponse(result=True, media_id=media.id)
