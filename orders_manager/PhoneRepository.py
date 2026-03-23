from typing import Any, Dict, List, Optional

from FastAPI_back.utils.repositories import BaseRepository
from FastAPI_back.utils.errors import AlreadyExistsError
from orders_manager.models import PhoneModelTable
from orders_manager.schemas import PhoneModelCreate
from orders_manager.schemas import PhoneModelResponse



class PhoneRepository(BaseRepository[PhoneModelTable]):
    
    schema_class = PhoneModelTable

    async def create(self, schema: PhoneModelCreate) -> PhoneModelResponse:
        # Ensure model_code is unique before attempting to insert
        instance: PhoneModelTable = await self._save(schema.model_dump())
        return PhoneModelResponse.model_validate(instance)
    
    