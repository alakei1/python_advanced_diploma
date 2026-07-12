"""
╔═════════════════════════════════════════════════════════════╗
║                                                             ║
║    ██╗    ██╗████████╗██╗████████╗████████╗███████╗██████╗  ║
║    ██║    ██║╚══██╔══╝██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗ ║
║    ██║ █╗ ██║   ██║   ██║   ██║      ██║   █████╗  ██████╔╝ ║
║    ██║███╗██║   ██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗ ║
║    ╚███╔███╔╝   ██║   ██║   ██║      ██║   ███████╗██║  ██║ ║
║     ╚══╝╚══╝    ╚═╝   ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝ ║
║                                                             ║
║             ██████╗██╗      ██████╗ ███╗   ██╗███████╗      ║
║            ██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝      ║
║            ██║     ██║     ██║   ██║██╔██╗ ██║█████╗        ║
║            ██║     ██║     ██║   ██║██║╚██╗██║██╔══╝        ║
║            ╚██████╗███████╗╚██████╔╝██║ ╚████║███████╗      ║
║             ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝      ║
║                                                             ║
║                    Version: 1.0.0                           ║
║                                                             ║
║           Developed by Alexey Lugachev                      ║
║                    (c) 2024                                 ║
║                                                             ║
║    Docs:  http://localhost:8000/docs                        ║
║    Redoc: http://localhost:8000/redoc                       ║
║                                                             ║
╚═════════════════════════════════════════════════════════════╝
Twitter Clone API
=============================================
Разработано Алексеем Лугачевым
GitHub: https://github.com/your-profile
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from config.config import settings_log
from scr.app.api.v1.endpoints import medias, tweets, users
from scr.core.logger import AppLogger, log_debug, log_error, log_info
from scr.schemas.error import ErrorResponse


# ============================================ #
# LIFECYCLE EVENTS                             #
# ============================================ #
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.

    Выполняется при старте и остановке сервера.
    """
    # ========== STARTUP ========== #
    await log_info("Starting Twitter Clone API...")
    await log_info(f"Upload directory: {settings_log.UPLOAD_DIR}")
    await log_info(f"Debug mode: {settings_log.DEBUG}")
    await log_info("Developed by Alexey Lugachev")

    # Создаем директорию для загрузок, если её нет
    os.makedirs(settings_log.UPLOAD_DIR, exist_ok=True)

    await log_info("Application started successfully!")

    yield  # Здесь работает приложение

    # ========== SHUTDOWN ========== #
    await log_info("Shutting down Twitter Clone API...")
    await log_info("Goodbye!")
    await AppLogger.shutdown()


# ============================================ #
# FASTAPI APP                                  #
# ============================================ #
app = FastAPI(
    title="Twitter Clone API",
    redirect_slashes=False,
    description="""
    ### Архитектура и возможности платформы

    Современное высокопроизводительное асинхронное API, реализующее базовую бизнес-логику социальной сети коротких сообщений (аналог Twitter). Сервис спроектирован с учетом требований к высокой скорости обработки запросов и предоставляет полный набор эндпоинтов для интеграции с веб-фронтендом или мобильными клиентами.

    ---

    ### Ключевой функционал системы

    * **Управление публикациями** — создание, чтение, пагинация и удаление твитов.
    * **Социальные взаимодействия** — атомарные операции установки лайков и отмены реакций.
    * **Граф подписок** — изоляция социальных связей, механика подписок и отписок между пользователями.
    * **Медиа-сервис** — изолированная загрузка изображений, валидация типов файлов и их последующая привязка к публикациям.
    * **Умная лента** — агрегация и динамическое построение персонализированной ленты активности на основе подписок.

    ---

    ### Инструкция по авторизации (Тестирование API)

    Для выполнения запросов к защищенным эндпоинтам необходимо пройти аутентификацию по токену:
    1. Нажмите кнопку **Authorize** в правом верхнем углу страницы Swagger.
    2. В поле **Value** введите предустановленный тестовый ключ: `test`
    3. Нажмите **Authorize**, затем **Close**. Все последующие тестовые запросы будут автоматически отправляться с необходимым заголовком.

    ---

    ### Технологический стек проекта

    * **Core Framework:** FastAPI (Python 3.11) + Uvicorn (ASGI-сервер).
    * **Data Access Layer:** SQLAlchemy 2.0 (Async Engine) + Драйвер `asyncpg`.
    * **Database & Migrations:** PostgreSQL 16 + Автоматические миграции схемы через Alembic.
    * **Infrastructure:** Docker Compose (Контейнеризация сервисов) + Nginx (Обратный прокси и раздача статического контента).

    ---
    * **Разработчик:** Алексей Лугачев  
    * **Тип проекта:** Дипломная работа повышенного уровня  
    * **Релиз:** 2026 год
    """,  # noqa: E501
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    contact={
        "name": "Alexey Lugachev",
        "url": "https://github.com",
        "email": "your-email@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org",
    },
)


UPLOAD_DIR = settings_log.UPLOAD_DIR  # или просто "./uploads"


os.makedirs(UPLOAD_DIR, exist_ok=True)


app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ============================================ #
# CORS MIDDLEWARE                              #
# ============================================ #
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================ #
# ROUTERS                                      #
# ============================================ #
app.include_router(tweets.router)
app.include_router(users.router)
app.include_router(medias.router)


# ============================================ #
# STATIC FILES                                 #
# ============================================ #
app.mount("/uploads", StaticFiles(directory=settings_log.UPLOAD_DIR), name="uploads")


# ============================================ #
# ROOT ENDPOINT                                #
# ============================================ #
@app.get("/")
async def root():
    """Корневой эндпоинт с информацией о сервисе."""
    await log_debug("Root endpoint called")
    return {
        "service": "Twitter Clone API",
        "version": "1.0.0",
        "developer": "Alexey Lugachev",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running",
    }


# ============================================ #
# EXCEPTION HANDLERS                           #
# ============================================ #
@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    """Обработчик HTTP ошибок от Starlette."""
    await log_error(
        f"HTTP {exc.status_code}: {exc.detail}",
        path=request.url.path,
        method=request.method,
    )
    # Приводим detail к строке, если он None
    error_message = str(exc.detail) if exc.detail is not None else "Unknown error"
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_type="http_error",
            error_message=error_message,
        ).model_dump(),
    )


@app.exception_handler(HTTPException)
async def fastapi_http_exception_handler(request: Request, exc: HTTPException):
    """Обработчик HTTP ошибок от FastAPI."""
    await log_error(
        f"HTTP {exc.status_code}: {exc.detail}",
        path=request.url.path,
        method=request.method,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_type=(
                exc.detail.__class__.__name__
                if hasattr(exc.detail, "__class__")
                else "HTTPException"
            ),
            error_message=str(exc.detail),
        ).model_dump(),  # Используем model_dump вместо dict
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Обработчик непредвиденных ошибок."""
    await log_error(
        f"Unhandled exception: {str(exc)}",
        path=request.url.path,
        method=request.method,
        exc_info=True,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error_type=exc.__class__.__name__,
            error_message="Internal server error. Please try again later.",
        ).model_dump(),  # Используем model_dump вместо dict
    )


# ============================================ #
# DEVELOPER INFO                               #
# ============================================ #
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "scr.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


__all__ = ["app"]
