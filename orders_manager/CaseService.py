from FastAPI_back.db.transactional import Transactional, Propagation
from orders_manager.CaseRepository import CaseRepository
from orders_manager.schemas import PhoneCaseTypeCreate, PhoneCaseTypeResponse


class CaseService:
    def __init__(
        self,
        case_repository: CaseRepository,
    ):
        self.case_repository = case_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_case_type(
            self, payload: dict,
    ) -> PhoneCaseTypeResponse:
        case_type = PhoneCaseTypeCreate(**payload)
        return await self.case_repository.create(case_type)
