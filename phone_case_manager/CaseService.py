from typing import List

from FastAPI_back.db.transactional import Transactional, Propagation
from phone_case_manager.CaseRepository import CaseRepository
from phone_case_manager.schemas import PhoneCaseTypeCreate, PhoneCaseTypeUpdate, PhoneCaseTypeResponse


class CaseService:
    def __init__(self, case_repository: CaseRepository):
        self.case_repository = case_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_case_type(self, payload: dict) -> PhoneCaseTypeResponse:
        case_type = PhoneCaseTypeCreate(**payload)
        return await self.case_repository.create(case_type)

    async def list_case_types(self) -> List[PhoneCaseTypeResponse]:
        return await self.case_repository.list_all()

    async def get_case_type(self, case_type_id: int) -> PhoneCaseTypeResponse:
        return await self.case_repository.get_by_id(case_type_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_case_type(self, case_type_id: int, payload: dict) -> PhoneCaseTypeResponse:
        update_payload = PhoneCaseTypeUpdate(**payload).model_dump(exclude_unset=True)
        return await self.case_repository.update(case_type_id, update_payload)

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_case_type(self, case_type_id: int) -> None:
        await self.case_repository.delete(case_type_id)
