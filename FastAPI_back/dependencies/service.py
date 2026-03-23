from typing import List, Type, TypeVar, Callable, Any, Coroutine
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import get_repository, RepositoryClass, get_session
from FastAPI_back.utils.services import BaseService

ServiceClass = TypeVar('ServiceClass', bound=BaseService)


# Factory function to get service with multiple repositories

def get_service(service_class: Type[ServiceClass], *repo_classes: Type[RepositoryClass]) -> Callable[
    [AsyncSession], Coroutine[Any, Any, ServiceClass]]:
    
    async def _get_service(session: AsyncSession = Depends(get_session)) -> ServiceClass:
        # Correctly instantiate repository instances
        repositories = [repo_class(session) for repo_class in repo_classes]
        return service_class(*repositories)

    return _get_service



