from typing import List

from FastAPI_back.db.transactional import Transactional, Propagation
from phone_case_manager.PhoneRepository import PhoneRepository
from phone_case_manager.schemas import PhoneCreate, PhoneUpdate, PhoneResponse


class PhoneService:
    def __init__(self, phone_repository: PhoneRepository):
        self.phone_repository = phone_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_phone_model(self, payload: dict) -> PhoneResponse:
        phone_model = PhoneCreate(**payload)
        return await self.phone_repository.create(phone_model)

    async def list_phone_models(self) -> List[PhoneResponse]:
        return await self.phone_repository.list_all()

    async def get_phone_model(self, phone_id: int) -> PhoneResponse:
        return await self.phone_repository.get_by_id(phone_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_phone_model(self, phone_id: int, payload: dict) -> PhoneResponse:
        update_payload = PhoneUpdate(**payload).model_dump(exclude_unset=True)
        return await self.phone_repository.update(phone_id, update_payload)

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_phone_model(self, phone_id: int) -> None:
        await self.phone_repository.delete(phone_id)
