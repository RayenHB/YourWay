from typing import List

from FastAPI_back.db.transactional import Transactional, Propagation
from phone_case_manager.PhoneService import PhoneService
from phone_case_manager.CaseService import CaseService
from phone_case_manager.PhoneCaseService import PhoneCaseService
from phone_case_manager.PhoneCaseTemplateService import PhoneCaseTemplateService
from phone_case_manager.PhoneRepository import PhoneRepository
from phone_case_manager.CaseRepository import CaseRepository
from phone_case_manager.PhoneCaseRepository import PhoneCaseRepository
from phone_case_manager.PhoneCaseTemplateRepository import PhoneCaseTemplateRepository
from FastAPI_back.utils.errors import NotFoundError
from phone_case_manager.schemas import (
    PhoneCreate,
    PhoneResponse,
    PhoneUpdate,
    PhoneCaseTypeCreate,
    PhoneCaseTypeResponse,
    PhoneCaseTypeUpdate,
    PhoneCaseCreate,
    PhoneCaseResponse,
    PhoneCaseUpdate,
    PhoneCaseTemplateCreate,
    PhoneCaseTemplateResponse,
    PhoneCaseTemplateUpdate,
    PhoneWithCaseResponse
)


class Service:
    def __init__(
        self,
        phone_repository: PhoneRepository,
        case_repository: CaseRepository,
        phone_case_repository: PhoneCaseRepository,
        template_repository: PhoneCaseTemplateRepository,
    ):
        self.phone_service = PhoneService(phone_repository)
        self.case_service = CaseService(case_repository)
        self.phone_case_service = PhoneCaseService(phone_case_repository)
        self.template_service = PhoneCaseTemplateService(template_repository)

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_phone_model(
        self,
        phone_payload: dict,
        case_type_payload: dict,
        phone_case_payload: dict,
        template_payload: dict | None,
    ) -> PhoneWithCaseResponse:
        case_type = await self.case_service.create_case_type(case_type_payload)
        if not case_type:
            raise ValueError("Failed to create case type")

        phone = await self.phone_service.create_phone_model(phone_payload)
        if not phone:
            raise ValueError("Failed to create phone model")

        phone_case_payload["phone_model_id"] = phone.id
        phone_case_payload["case_type_id"] = case_type.id

        phone_case = await self.phone_case_service.create_phone_case(phone_case_payload)
        if not phone_case:
            raise ValueError("Failed to create phone case")

        template = None
        if template_payload:
            template_payload["phone_case_id"] = phone_case.id
            template = await self.template_service.create_template(template_payload)

        return PhoneWithCaseResponse(
            phone_model=phone,
            case_type=case_type,
            phone_case=phone_case,
            template=template,
        )

    async def list_phone_models(self) -> List[PhoneResponse]:
        return await self.phone_service.list_phone_models()

    async def get_phone_model(self, phone_id: int) -> PhoneResponse:
        return await self.phone_service.get_phone_model(phone_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_phone_model(self, phone_id: int, payload: dict) -> PhoneResponse:
        return await self.phone_service.update_phone_model(phone_id, payload)

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_phone_model(self, phone_id: int) -> None:
        await self.phone_service.delete_phone_model(phone_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_case_type(self, payload: dict) -> PhoneCaseTypeResponse:
        return await self.case_service.create_case_type(payload)

    async def list_case_types(self) -> List[PhoneCaseTypeResponse]:
        return await self.case_service.list_case_types()

    async def get_case_type(self, case_type_id: int) -> PhoneCaseTypeResponse:
        return await self.case_service.get_case_type(case_type_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_case_type(self, case_type_id: int, payload: dict) -> PhoneCaseTypeResponse:
        return await self.case_service.update_case_type(case_type_id, payload)

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_case_type(self, case_type_id: int) -> None:
        await self.case_service.delete_case_type(case_type_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_phone_case(self, payload: dict) -> PhoneCaseResponse:
        phone_model_id = payload.get("phone_model_id")
        case_type_id = payload.get("case_type_id")
        if phone_model_id is None or case_type_id is None:
            raise NotFoundError(message="phone_model_id and case_type_id are required")

        await self.phone_service.get_phone_model(phone_model_id)
        await self.case_service.get_case_type(case_type_id)
        return await self.phone_case_service.create_phone_case(payload)

    async def list_phone_cases(self) -> List[PhoneCaseResponse]:
        return await self.phone_case_service.list_phone_cases()

    async def get_phone_case(self, phone_case_id: int) -> PhoneCaseResponse:
        return await self.phone_case_service.get_phone_case(phone_case_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_phone_case(self, phone_case_id: int, payload: dict) -> PhoneCaseResponse:
        phone_model_id = payload.get("phone_model_id")
        case_type_id = payload.get("case_type_id")
        if phone_model_id is not None:
            await self.phone_service.get_phone_model(phone_model_id)
        if case_type_id is not None:
            await self.case_service.get_case_type(case_type_id)
        return await self.phone_case_service.update_phone_case(phone_case_id, payload)

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_phone_case(self, phone_case_id: int) -> None:
        await self.phone_case_service.delete_phone_case(phone_case_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_template(self, payload: dict) -> PhoneCaseTemplateResponse:
        phone_case_id = payload.get("phone_case_id")
        if phone_case_id is None:
            raise NotFoundError(message="phone_case_id is required")
        await self.phone_case_service.get_phone_case(phone_case_id)
        return await self.template_service.create_template(payload)

    async def list_templates(self) -> List[PhoneCaseTemplateResponse]:
        return await self.template_service.list_templates()

    async def get_template(self, template_id: int) -> PhoneCaseTemplateResponse:
        return await self.template_service.get_template(template_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_template(self, template_id: int, payload: dict) -> PhoneCaseTemplateResponse:
        phone_case_id = payload.get("phone_case_id")
        if phone_case_id is not None:
            await self.phone_case_service.get_phone_case(phone_case_id)
        return await self.template_service.update_template(template_id, payload)

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_template(self, template_id: int) -> None:
        await self.template_service.delete_template(template_id)
