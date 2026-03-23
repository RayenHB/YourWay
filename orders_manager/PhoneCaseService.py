from typing import List, Optional

from FastAPI_back.db.transactional import Transactional, Propagation
from orders_manager.PhoneCaseRepository import PhoneCaseRepository
from orders_manager.schemas import PhoneCaseCreate, PhoneCaseResponse


class PhoneCaseService:
    def __init__(self, phone_case_repository: PhoneCaseRepository):
        self.phone_case_repository = phone_case_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_phone_case(self, payload: dict) -> PhoneCaseResponse:
        phone_case = PhoneCaseCreate(**payload)
        return await self.phone_case_repository.create(phone_case)

    async def get_phone_case(self, phone_case_id: int) -> Optional[PhoneCaseResponse]:
        return await self.phone_case_repository.get_by_id(phone_case_id)

    async def list_phone_cases(self) -> List[PhoneCaseResponse]:
        return await self.phone_case_repository.list_all()
