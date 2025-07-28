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


settings = Settings()
