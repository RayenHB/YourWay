from typing import List, Optional

from FastAPI_back.utils.repositories import BaseRepository
from orders_manager.models import PhoneCaseTable
from orders_manager.schemas import PhoneCaseCreate, PhoneCaseResponse


class PhoneCaseRepository(BaseRepository[PhoneCaseTable]):
    schema_class = PhoneCaseTable

    async def create(self, schema: PhoneCaseCreate) -> PhoneCaseResponse:
        instance: PhoneCaseTable = await self._save(schema.model_dump())
        return PhoneCaseResponse.model_validate(instance)

    async def get_by_id(self, phone_case_id: int) -> Optional[PhoneCaseResponse]:
        instance = await self._get(id_=phone_case_id)
        return PhoneCaseResponse.model_validate(instance)

    async def list_all(self) -> List[PhoneCaseResponse]:
        results: List[PhoneCaseResponse] = []
        async for instance in self._all_with_filters(order_by=PhoneCaseTable.created_at.desc()):
            results.append(PhoneCaseResponse.model_validate(instance))
        return results
