from contextvars import ContextVar, Token
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from FastAPI_back.configuration.config import get_app_settings
from FastAPI_back.db.engine import create_engine

session_context: ContextVar[AsyncSession] = ContextVar('session_context')


def set_session_context(session_id: AsyncSession) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


settings = get_app_settings()
engine = create_engine()

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)
