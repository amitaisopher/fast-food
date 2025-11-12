from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal

EnvironmentType = Literal["development", "production", "testing"]


class Settings(BaseSettings):
    """
    Application settings.
    """
    environment: EnvironmentType = Field(default="development",)
    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")
    sentry_enabled: bool = Field(default=False, alias="SENTRY_ENABLED")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


_settings = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings