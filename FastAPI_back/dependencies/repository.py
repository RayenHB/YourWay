from contextlib import asynccontextmanager
from typing import Type, TypeVar, Callable, AsyncGenerator, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from FastAPI_back.db.session import SessionLocal, session_context

from FastAPI_back.utils.repositories import BaseRepository

RepositoryClass = TypeVar('RepositoryClass', bound=BaseRepository)

__all__ = ("get_session", "get_repository", "RepositoryClass", "get_session_v2")


# Dependency to get a new session for each request
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        token = session_context.set(session)
        print(f"Session created: {session}")
        try:
            yield session
        finally:
            session_context.reset(token)
            print("Session closed")


@asynccontextmanager
async def get_session_v2() -> AsyncSession:
    async with SessionLocal() as session:
        token = session_context.set(session)
        try:
            yield session
        finally:
            session_context.reset(token)


# Factory function to get repository with session

def get_repository(repo_class: Type[RepositoryClass]) -> Callable[[AsyncSession], RepositoryClass]:
    def _get_repository(session: AsyncSession = Depends(get_session)) -> RepositoryClass:
        return repo_class(session=session)

    return _get_repository

