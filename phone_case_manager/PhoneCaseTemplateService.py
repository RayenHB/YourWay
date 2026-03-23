from typing import List

from FastAPI_back.db.transactional import Transactional, Propagation
from phone_case_manager.PhoneCaseTemplateRepository import PhoneCaseTemplateRepository
from phone_case_manager.schemas import (
    PhoneCaseTemplateCreate,
    PhoneCaseTemplateUpdate,
    PhoneCaseTemplateResponse,
)


class PhoneCaseTemplateService:
    def __init__(self, template_repository: PhoneCaseTemplateRepository):
        self.template_repository = template_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_template(self, payload: dict) -> PhoneCaseTemplateResponse:
        template = PhoneCaseTemplateCreate(**payload)
        return await self.template_repository.create(template)

    async def list_templates(self) -> List[PhoneCaseTemplateResponse]:
        return await self.template_repository.list_all()

    async def get_template(self, template_id: int) -> PhoneCaseTemplateResponse:
        return await self.template_repository.get_by_id(template_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_template(self, template_id: int, payload: dict) -> PhoneCaseTemplateResponse:
        update_payload = PhoneCaseTemplateUpdate(**payload).model_dump(exclude_unset=True)
        return await self.template_repository.update(template_id, update_payload)

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_template(self, template_id: int) -> None:
        await self.template_repository.delete(template_id)
