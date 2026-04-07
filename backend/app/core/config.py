"""Application configuration using Pydantic settings."""
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Centralized application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore")

    database_url: str = Field(...)
    jwt_secret_key: str = Field(...)
    jwt_algorithm: str = Field("HS256")
    redis_url: str = Field("redis://localhost:6379/0")
    celery_broker_url: str | None = Field(default=None)
    celery_result_backend: str | None = Field(default=None)
    reminder_minutes_before: int = Field(60, ge=1, le=10080)
    enable_background_reminders: bool = Field(True)
    bootstrap_reminders_on_startup: bool = Field(True)
    reminder_processing_timeout_minutes: int = Field(15, ge=1, le=1440)
    cors_origins: str = Field("http://localhost:5173,http://127.0.0.1:5173")
    access_token_expire_minutes: int = Field(60, ge=5, le=1440)
    refresh_token_expire_days: int = Field(30, ge=1, le=365)
    refresh_cookie_name: str = Field("booking_refresh_token")
    refresh_cookie_secure: bool = Field(False)
    refresh_cookie_samesite: str = Field("lax")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance to avoid re-parsing environment variables."""

    return Settings()  # pyright: ignore[reportCallIssue]


settings = get_settings()
