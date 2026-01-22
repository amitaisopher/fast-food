from typing import AsyncGenerator

from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()
database_url = make_url(settings.database_url)

engine_kwargs = {}
if database_url.get_backend_name() == "sqlite":
    engine_kwargs["connect_args"] = {
        "check_same_thread": False  # Needed for SQLite to allow usage in multiple threads
    }

engine = create_async_engine(settings.database_url, **engine_kwargs)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
