from typing import List

from FastAPI_back.db.transactional import Transactional, Propagation
from phone_case_manager.PhoneCaseRepository import PhoneCaseRepository
from phone_case_manager.schemas import PhoneCaseCreate, PhoneCaseUpdate, PhoneCaseResponse


class PhoneCaseService:
    def __init__(self, phone_case_repository: PhoneCaseRepository):
        self.phone_case_repository = phone_case_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_phone_case(self, payload: dict) -> PhoneCaseResponse:
        phone_case = PhoneCaseCreate(**payload)
        return await self.phone_case_repository.create(phone_case)

    async def list_phone_cases(self) -> List[PhoneCaseResponse]:
        return await self.phone_case_repository.list_all()

    async def get_phone_case(self, phone_case_id: int) -> PhoneCaseResponse:
        return await self.phone_case_repository.get_by_id(phone_case_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_phone_case(self, phone_case_id: int, payload: dict) -> PhoneCaseResponse:
        update_payload = PhoneCaseUpdate(**payload).model_dump(exclude_unset=True)
        return await self.phone_case_repository.update(phone_case_id, update_payload)

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_phone_case(self, phone_case_id: int) -> None:
        await self.phone_case_repository.delete(phone_case_id)
