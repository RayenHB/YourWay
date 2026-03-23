from typing import List

from FastAPI_back.utils.repositories import BaseRepository
from phone_case_manager.models import PhoneModelTable
from phone_case_manager.schemas import PhoneCreate, PhoneResponse

class PhoneRepository(BaseRepository[PhoneModelTable]):
    schema_class = PhoneModelTable

    async def create(self, schema: PhoneCreate) -> PhoneResponse:
        instance: PhoneModelTable = await self._save(schema.model_dump())
        return PhoneResponse.model_validate(instance)

    async def list_all(self) -> List[PhoneResponse]:
        results: List[PhoneResponse] = []
        async for instance in self._all_with_filters(
            order_by=PhoneModelTable.created_at.desc(),
        ):
            results.append(PhoneResponse.model_validate(instance))
        return results

    async def get_by_id(self, phone_id: int) -> PhoneResponse:
        instance = await self._get(id_=phone_id)
        return PhoneResponse.model_validate(instance)

    async def update(self, phone_id: int, payload: dict) -> PhoneResponse:
        instance = await self._update("id", phone_id, payload)
        return PhoneResponse.model_validate(instance)

    async def delete(self, phone_id: int) -> None:
        await self._delete(phone_id)
