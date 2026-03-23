from typing import List

from FastAPI_back.utils.repositories import BaseRepository
from phone_case_manager.models import PhoneCaseTemplateTable
from phone_case_manager.schemas import PhoneCaseTemplateCreate, PhoneCaseTemplateResponse


class PhoneCaseTemplateRepository(BaseRepository[PhoneCaseTemplateTable]):
    schema_class = PhoneCaseTemplateTable

    async def create(self, schema: PhoneCaseTemplateCreate) -> PhoneCaseTemplateResponse:
        instance: PhoneCaseTemplateTable = await self._save(schema.model_dump())
        return PhoneCaseTemplateResponse.model_validate(instance)

    async def list_all(self) -> List[PhoneCaseTemplateResponse]:
        results: List[PhoneCaseTemplateResponse] = []
        async for instance in self._all_with_filters(
            order_by=PhoneCaseTemplateTable.created_at.desc(),
        ):
            results.append(PhoneCaseTemplateResponse.model_validate(instance))
        return results

    async def get_by_id(self, template_id: int) -> PhoneCaseTemplateResponse:
        instance = await self._get(id_=template_id)
        return PhoneCaseTemplateResponse.model_validate(instance)

    async def update(self, template_id: int, payload: dict) -> PhoneCaseTemplateResponse:
        instance = await self._update("id", template_id, payload)
        return PhoneCaseTemplateResponse.model_validate(instance)

    async def delete(self, template_id: int) -> None:
        await self._delete(template_id)
