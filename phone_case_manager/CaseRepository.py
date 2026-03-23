from typing import List

from FastAPI_back.utils.repositories import BaseRepository
from phone_case_manager.models import PhoneCaseTypeTable
from phone_case_manager.schemas import PhoneCaseTypeCreate, PhoneCaseTypeResponse


class CaseRepository(BaseRepository[PhoneCaseTypeTable]):
    schema_class = PhoneCaseTypeTable

    async def create(self, schema: PhoneCaseTypeCreate) -> PhoneCaseTypeResponse:
        instance: PhoneCaseTypeTable = await self._save(schema.model_dump())
        return PhoneCaseTypeResponse.model_validate(instance)

    async def list_all(self) -> List[PhoneCaseTypeResponse]:
        results: List[PhoneCaseTypeResponse] = []
        async for instance in self._all_with_filters(
            order_by=PhoneCaseTypeTable.created_at.desc(),
        ):
            results.append(PhoneCaseTypeResponse.model_validate(instance))
        return results

    async def get_by_id(self, case_type_id: int) -> PhoneCaseTypeResponse:
        instance = await self._get(id_=case_type_id)
        return PhoneCaseTypeResponse.model_validate(instance)

    async def update(self, case_type_id: int, payload: dict) -> PhoneCaseTypeResponse:
        instance = await self._update("id", case_type_id, payload)
        return PhoneCaseTypeResponse.model_validate(instance)

    async def delete(self, case_type_id: int) -> None:
        await self._delete(case_type_id)
