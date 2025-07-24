from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, Union, Literal

EnvironmentType = Literal["development", "production", "testing"]

class Settings(BaseSettings):
    """
    Application settings.
    """
    environment: EnvironmentType = Field(default="development",)


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


settings = Settings()