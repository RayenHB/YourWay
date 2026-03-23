from typing import Any, Dict, List,Optional

from FastAPI_back.utils.repositories import BaseRepository
from users_manager.models import (
UserTable
)
from users_manager.schemas import (
UserFlat,UserUncommited
)




class UserRepository(BaseRepository[UserTable]):
    
    schema_class = UserTable
    

    async def all_paginated(
        self, page: int, page_size: int, filters: Dict[str, Any]
    ) -> Dict[str, Any]:
        paginated_result = await self._all_paginated(
            page=page,
            page_size=page_size,
            filters=filters,
            relationships=[]
        )
        items = paginated_result["result"]
        paginated_result["result"] = [
            UserFlat.model_validate(item) for item in items
        ]
        return paginated_result

    async def get(self, id_: int) -> UserFlat:
        result: UserTable = await self._get(id_,relationships=[])
        return UserFlat.model_validate(result)

    async def create(self, schema: UserUncommited) -> UserFlat:
        instance: UserTable = await self._save(schema.model_dump())
        return UserFlat.model_validate(instance)


    async def update(self, id_: int, payload: Dict[str, Any]) -> UserFlat:
        instance = await self._update("id", id_, payload)
        return UserFlat.model_validate(instance)

    async def delete(self, id_: int) -> None:
        await self._delete(id_)

    async def exists(self, filters : Dict[str, Any],exclude_id: Optional[Any] = None,
        operator: Optional[str] = "OR") -> bool:
        return await self._exists(filters,exclude_id,operator)
    
    async def get_all(self, filters: Dict[str, Any] = None) -> list[UserFlat]:
        all_users = [
            UserFlat.model_validate(item)
            async for item in self._all_with_filters(filters=filters, relationships=[])
        ]
        return all_users
    async def find(self, filters: Dict[str, Any] = None, relationships: Optional[List[str]] = None)-> UserFlat:
        instance = await self.find_by(filters, relationships)
        return UserFlat.model_validate(instance)






