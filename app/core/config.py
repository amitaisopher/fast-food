from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal
import os
from enum import StrEnum


class EnvironmentType(StrEnum):
    """Enum for application environments."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    STAGING = "staging"


def get_env_file_name():
    app_env: str = os.getenv("APP_ENV", EnvironmentType.DEVELOPMENT.value)
    env_file = f".env.{app_env}"
    return env_file


class Settings(BaseSettings):
    """
    Application settings.
    """
    environment: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT,)
    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")
    sentry_enabled: bool = Field(default=False, alias="SENTRY_ENABLED")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

    model_config = SettingsConfigDict(
        env_file=get_env_file_name(), extra="ignore", env_file_encoding="utf-8"
    )


_settings = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings