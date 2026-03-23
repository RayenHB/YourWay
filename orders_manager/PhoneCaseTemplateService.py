from typing import Optional

from FastAPI_back.db.transactional import Transactional, Propagation
from orders_manager.PhoneCaseTemplateRepository import PhoneCaseTemplateRepository
from orders_manager.schemas import PhoneCaseTemplateCreate, PhoneCaseTemplateUpdate, PhoneCaseTemplateResponse


class PhoneCaseTemplateService:
    def __init__(self, template_repository: PhoneCaseTemplateRepository):
        self.template_repository = template_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_template(self, payload: dict) -> PhoneCaseTemplateResponse:
        template = PhoneCaseTemplateCreate(**payload)
        return await self.template_repository.create(template)

    async def get_template(self, phone_case_id: int) -> Optional[PhoneCaseTemplateResponse]:
        return await self.template_repository.get_by_phone_case_id(phone_case_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_template(self, phone_case_id: int, payload: dict) -> PhoneCaseTemplateResponse:
        update_payload = PhoneCaseTemplateUpdate(**payload).model_dump(exclude_unset=True)
        return await self.template_repository.update_by_phone_case_id(phone_case_id, update_payload)
