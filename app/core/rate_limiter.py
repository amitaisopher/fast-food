from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.redis import get_redis, get_redis_url
from redis.asyncio import Redis


# Create a Redis client (async)
redis_client: Redis = get_redis()

# Initialize SlowAPI limiter with Redis storage
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=get_redis_url(),
)
