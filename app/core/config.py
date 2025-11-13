from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Any
import os
from enum import StrEnum


class Environment(StrEnum):
    """Enum for application environments."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    STAGING = "staging"


def get_env_file_name():
    app_env: str = os.getenv("APP_ENV", Environment.DEVELOPMENT.value)
    env_file = f".env.{app_env}"
    return env_file


class Settings(BaseSettings):
    """
    Application settings.
    """

    def __init__(self, **data):
        super().__init__(**data)

    environment: Environment = Field(default=Environment.DEVELOPMENT,)
    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")
    sentry_enabled: bool = Field(default=False, alias="SENTRY_ENABLED")

    # Redis config
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_password: str | None = Field(default=None, alias="REDIS_PASSWORD")

    @field_validator("redis_port", mode="before")
    @classmethod
    def validate_redis_port(cls, v: Any) -> int:
        """Validate and convert REDIS_PORT to integer, handling empty strings."""
        if v == "" or v is None:
            return 6379  # Return default value
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                return 6379  # Return default value if conversion fails
        return 6379
    

    @property
    def redis_url(self) -> str:
        """Construct the Redis URL if host and password are provided. For production use rediss."""
        if not self.redis_host or not self.redis_password:
            raise ValueError("Redis host or password is not configured")
        if self.environment == Environment.DEVELOPMENT:
            return f"redis://default:{self.redis_password}@{self.redis_host}:{self.redis_port}"
        else:
            return f"rediss://default:{self.redis_password}@{self.redis_host}:{self.redis_port}"

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
        app_env: str = os.getenv("ENVIRONMENT", Environment.DEVELOPMENT.value)
        env_file = f".env.{app_env}"
        _settings = Settings(_env_file=env_file)
    return _settings