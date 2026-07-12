"""Асинхронный сервис для работы с медиафайлами."""

import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import settings_log
from scr.database.models import Media


class MediaService:
    """Асинхронный сервис для работы с медиафайлами."""

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_media(self, file: UploadFile, user_id: int) -> Media:
        """
        Сохранить медиафайл (асинхронно).

        Args:
            file: Загружаемый файл
            user_id: ID пользователя, загружающего файл (не используется в БД,
                     но может понадобиться для аудита в будущем)

        Returns:
            Media: Созданный объект медиа

        Raises:
            HTTPException: Если файл невалидный
        """
        # user_id пока не используется, но оставляем для совместимости
        # В будущем можно добавить поле user_id в модель Media
        _ = user_id  # noqa: F841

        # Проверяем content-type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image",
            )

        # Проверяем расширение
        file_extension = os.path.splitext(file.filename or "")[1].lower()
        if file_extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File extension not allowed. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}",  # noqa: E501
            )

        # Проверяем размер
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        if file_size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {self.MAX_FILE_SIZE // 1024 // 1024} MB",  # noqa: E501
            )

        # Генерируем уникальное имя файла
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Используем Path для безопасной работы с путями
        upload_dir = Path(settings_log.UPLOAD_DIR)
        file_path = upload_dir / unique_filename

        # Сохраняем файл
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Создаем запись в БД (без user_id, так как в модели его нет)
        media = Media(
            filename=file.filename or "unknown.jpg",
            file_path=unique_filename,
            tweet_id=None,  # Пока не привязан к твиту
        )
        self.db.add(media)
        await self.db.commit()
        await self.db.refresh(media)

        return media

    async def delete_media(self, media_id: int) -> bool:
        """
        Удалить медиафайл (асинхронно).

        Args:
            media_id: ID медиафайла

        Returns:
            bool: True если удаление успешно
        """
        media = await self.db.get(Media, media_id)
        if not media:
            return False

        # Удаляем файл с диска
        if media.file_path:
            upload_dir = Path(settings_log.UPLOAD_DIR)
            file_path = upload_dir / media.file_path
            if file_path.exists():
                try:
                    file_path.unlink()  # Удаляем файл
                except OSError:
                    # Логируем ошибку, но продолжаем
                    pass

        await self.db.delete(media)
        await self.db.commit()
        return True
