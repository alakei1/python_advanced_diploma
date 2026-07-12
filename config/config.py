import os

from dotenv import load_dotenv

# Загружаем .env, но только для тех переменных, которых ЕЩЕ НЕТ в системе.
# override=False не позволит файлу .env стереть настройки Docker.
load_dotenv(override=False)


class SettingsData:
    """Настройки базы данных."""

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "twitter_clone")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

    @property
    def database_url(self) -> str:

        env_url = os.getenv("DATABASE_URL")
        if env_url:
            return env_url

        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class SettingsLog:
    """Настройки логгера и приложения."""

    LOG_DIR = os.getenv("LOG_DIR", "./logs")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
    DEBUG = os.getenv("DEBUG", "True") == "True"


setting_data = SettingsData()
settings_log = SettingsLog()
