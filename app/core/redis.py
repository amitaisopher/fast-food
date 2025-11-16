from typing import Literal
from app.core.config import get_settings, Environment
import redis.asyncio as redis

settings = get_settings()
host = (settings.redis_host,)
port = (settings.redis_port,)
password = (settings.redis_password,)
ssl = (False if settings.environment == Environment.DEVELOPMENT else True,)


def get_redis_url() -> str:
    """
    Construct and return the Redis URL based on settings.
    """
    protocol: Literal["redis"] | Literal["rediss"] = (
        "redis" if settings.environment == Environment.DEVELOPMENT else "rediss"
    )
    password_part = f":{settings.redis_password}@" if settings.redis_password else ""
    return f"{protocol}://{password_part}{settings.redis_host}:{settings.redis_port}"


_redis = None


def get_redis() -> redis.Redis:
    """
    Get a Redis client instance.
    Initializes the client if it hasn't been created yet.
    """
    global _redis
    if _redis is None:
        _redis = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            ssl=False if settings.environment == Environment.DEVELOPMENT else True,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis
