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

    def __init__(self, **data):
        super().__init__(**data)

    environment: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT,)
    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")
    sentry_enabled: bool = Field(default=False, alias="SENTRY_ENABLED")

    model_config = SettingsConfigDict(
        env_file=get_env_file_name(), extra="ignore", env_file_encoding="utf-8"
    )


_settings = None


def get_settings() -> Settings:
    """
    Get the application settings.

    This function reads the ENVIRONMENT environment variable to determine which .env file to load.
    It defaults to 'development' if ENVIRONMENT is not set.
    """
    global _settings
    if _settings is None:
        app_env: str = os.getenv("ENVIRONMENT", EnvironmentType.DEVELOPMENT.value)
        env_file = f".env.{app_env}"
        _settings = Settings(_env_file=env_file)
    return _settings