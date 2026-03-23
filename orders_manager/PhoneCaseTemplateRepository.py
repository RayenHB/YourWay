from typing import Optional

from FastAPI_back.utils.repositories import BaseRepository
from orders_manager.models import PhoneCaseTemplateTable
from orders_manager.schemas import PhoneCaseTemplateCreate, PhoneCaseTemplateResponse


class PhoneCaseTemplateRepository(BaseRepository[PhoneCaseTemplateTable]):
    schema_class = PhoneCaseTemplateTable

    async def create(self, schema: PhoneCaseTemplateCreate) -> PhoneCaseTemplateResponse:
        instance: PhoneCaseTemplateTable = await self._save(schema.model_dump())
        return PhoneCaseTemplateResponse.model_validate(instance)

    async def get_by_phone_case_id(self, phone_case_id: int) -> Optional[PhoneCaseTemplateResponse]:
        instance = await self.find_by(filters={"phone_case_id": phone_case_id})
        return PhoneCaseTemplateResponse.model_validate(instance) if instance else None

    async def update_by_phone_case_id(self, phone_case_id: int, payload: dict) -> PhoneCaseTemplateResponse:
        instance = await self._update("phone_case_id", phone_case_id, payload)
        return PhoneCaseTemplateResponse.model_validate(instance)
