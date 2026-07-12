from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.logger import log_debug, log_error, log_info
from scr.database.database import get_db
from scr.database.models.user import User

api_key_header = APIKeyHeader(name="api-key", auto_error=False)

# Исправление для Ruff: выносим Depends в константы
_db_dep = Depends(get_db)
_api_key_dep = Depends(api_key_header)


async def get_current_user(
    db: AsyncSession = _db_dep,  # type: ignore
    api_key: str = _api_key_dep,  # type: ignore
) -> User:
    """Получение текущего пользователя по API ключу."""
    if not api_key:
        await log_error("API key required but not provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="API key required"
        )

    await log_debug(f"Authenticating with API key: {api_key[:8]}...")

    result = await db.execute(
        select(User).where(User.api_key == api_key)  # type: ignore[comparison-overlap]
    )
    user: User | None = result.scalar_one_or_none()

    if user is None:
        await log_error(f"Invalid API key: {api_key[:8]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )

    await log_info(f"User authenticated: {user.name} (ID: {user.id})")
    return user
