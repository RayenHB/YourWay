from typing import List

from FastAPI_back.utils.repositories import BaseRepository
from phone_case_manager.models import PhoneCaseTable
from phone_case_manager.schemas import PhoneCaseCreate, PhoneCaseResponse


class PhoneCaseRepository(BaseRepository[PhoneCaseTable]):
    schema_class = PhoneCaseTable

    async def create(self, schema: PhoneCaseCreate) -> PhoneCaseResponse:
        instance: PhoneCaseTable = await self._save(schema.model_dump())
        return PhoneCaseResponse.model_validate(instance)

    async def list_all(self) -> List[PhoneCaseResponse]:
        results: List[PhoneCaseResponse] = []
        async for instance in self._all_with_filters(
            order_by=PhoneCaseTable.created_at.desc(),
        ):
            results.append(PhoneCaseResponse.model_validate(instance))
        return results

    async def get_by_id(self, phone_case_id: int) -> PhoneCaseResponse:
        instance = await self._get(id_=phone_case_id)
        return PhoneCaseResponse.model_validate(instance)

    async def update(self, phone_case_id: int, payload: dict) -> PhoneCaseResponse:
        instance = await self._update("id", phone_case_id, payload)
        return PhoneCaseResponse.model_validate(instance)

    async def delete(self, phone_case_id: int) -> None:
        await self._delete(phone_case_id)
