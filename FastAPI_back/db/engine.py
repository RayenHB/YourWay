from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from FastAPI_back.configuration.config import get_app_settings

__all__ = ("create_engine",)


@lru_cache(maxsize=1)
def create_engine() -> AsyncEngine:
    """Create a new async database engine.
    A function result is cached since there is not reason to
    initiate the engine more than once since session is created
    for each separate transaction if needed.
    """
    settings = get_app_settings()
    return create_async_engine(
        settings.database_url.unicode_string(),
        future=True,
        pool_pre_ping=True,
        echo=False,
        pool_recycle=3600,
        pool_size=100,
        max_overflow=0,
        
    )
