from typing import Any, Dict, List, Optional

from FastAPI_back.utils.repositories import BaseRepository
from orders_manager.models import PhoneCaseTypeTable
from orders_manager.schemas import PhoneCaseTypeCreate,PhoneCaseTypeResponse



class CaseRepository(BaseRepository[PhoneCaseTypeTable]):
    schema_class = PhoneCaseTypeTable
    
    async def create(self, schema: PhoneCaseTypeCreate) -> PhoneCaseTypeResponse:
        instance: PhoneCaseTypeTable = await self._save(schema.model_dump())
        return PhoneCaseTypeResponse.model_validate(instance)
