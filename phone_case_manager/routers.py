from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv

from FastAPI_back.dependencies.service import get_service
from FastAPI_back.utils.response import Response, ResponseMulti
from phone_case_manager.PhoneRepository import PhoneRepository
from phone_case_manager.CaseRepository import CaseRepository
from phone_case_manager.PhoneCaseRepository import PhoneCaseRepository
from phone_case_manager.PhoneCaseTemplateRepository import PhoneCaseTemplateRepository
from phone_case_manager.Service import Service
from phone_case_manager.schemas import (
    PhoneCreate,
    PhoneUpdate,
    PhoneResponse,
    PhoneCaseTypeCreate,
    PhoneCaseTypeUpdate,
    PhoneCaseTypeResponse,
    PhoneCaseCreate,
    PhoneCaseUpdate,
    PhoneCaseResponse,
    PhoneCaseTemplateCreate,
    PhoneCaseTemplateUpdate,
    PhoneCaseTemplateResponse,
    CreatePhoneWithCase,
    PhoneWithCaseResponse
)


phone_case_router = APIRouter(prefix="")


@cbv(phone_case_router)
class PhoneCaseRouter:
    service: Service = Depends(
        get_service(
            Service,
            PhoneRepository,
            CaseRepository,
            PhoneCaseRepository,
            PhoneCaseTemplateRepository,
        )
    )

    @phone_case_router.post(
        "/phone-models",
        response_model=Response[PhoneWithCaseResponse],
        status_code=status.HTTP_201_CREATED,
    )
    async def create_phone_model(self, payload: CreatePhoneWithCase) -> Response[PhoneWithCaseResponse]:
        result = await self.service.create_phone_model(
            payload.phone_payload.model_dump(),
            payload.case_type_payload.model_dump(),
            payload.phone_case_payload.model_dump(),
            payload.template_payload.model_dump() if payload.template_payload else None,
        )
        return Response[PhoneWithCaseResponse](result=result)
    @phone_case_router.get(
        "/phone-models",
        response_model=ResponseMulti[PhoneResponse],
        status_code=status.HTTP_200_OK,
    )
    async def list_phone_models(self) -> ResponseMulti[PhoneResponse]:
        results = await self.service.list_phone_models()
        return ResponseMulti[PhoneResponse](result=results)

    @phone_case_router.get(
        "/phone-models/{phone_id}",
        response_model=Response[PhoneResponse],
        status_code=status.HTTP_200_OK,
    )
    async def get_phone_model(self, phone_id: int) -> Response[PhoneResponse]:
        result = await self.service.get_phone_model(phone_id)
        return Response[PhoneResponse](result=result)

    @phone_case_router.put(
        "/phone-models/{phone_id}",
        response_model=Response[PhoneResponse],
        status_code=status.HTTP_200_OK,
    )
    async def update_phone_model(
        self, phone_id: int, payload: PhoneUpdate
    ) -> Response[PhoneResponse]:
        result = await self.service.update_phone_model(
            phone_id, payload.model_dump(exclude_unset=True)
        )
        return Response[PhoneResponse](result=result)

    @phone_case_router.delete(
        "/phone-models/{phone_id}",
        response_model=None,
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_phone_model(self, phone_id: int):
        await self.service.delete_phone_model(phone_id)
        return None


    @phone_case_router.get(
        "/case-types",
        response_model=ResponseMulti[PhoneCaseTypeResponse],
        status_code=status.HTTP_200_OK,
    )
    async def list_case_types(self) -> ResponseMulti[PhoneCaseTypeResponse]:
        results = await self.service.list_case_types()
        return ResponseMulti[PhoneCaseTypeResponse](result=results)

    @phone_case_router.get(
        "/case-types/{case_type_id}",
        response_model=Response[PhoneCaseTypeResponse],
        status_code=status.HTTP_200_OK,
    )
    async def get_case_type(self, case_type_id: int) -> Response[PhoneCaseTypeResponse]:
        result = await self.service.get_case_type(case_type_id)
        return Response[PhoneCaseTypeResponse](result=result)

    @phone_case_router.put(
        "/case-types/{case_type_id}",
        response_model=Response[PhoneCaseTypeResponse],
        status_code=status.HTTP_200_OK,
    )
    async def update_case_type(
        self, case_type_id: int, payload: PhoneCaseTypeUpdate
    ) -> Response[PhoneCaseTypeResponse]:
        result = await self.service.update_case_type(
            case_type_id, payload.model_dump(exclude_unset=True)
        )
        return Response[PhoneCaseTypeResponse](result=result)

    @phone_case_router.delete(
        "/case-types/{case_type_id}",
        response_model=None,
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_case_type(self, case_type_id: int):
        await self.service.delete_case_type(case_type_id)
        return None

    @phone_case_router.post(
        "/phone-cases",
        response_model=Response[PhoneCaseResponse],
        status_code=status.HTTP_201_CREATED,
    )
    async def create_phone_case(self, payload: PhoneCaseCreate) -> Response[PhoneCaseResponse]:
        result = await self.service.create_phone_case(payload.model_dump())
        return Response[PhoneCaseResponse](result=result)

    @phone_case_router.get(
        "/phone-cases",
        response_model=ResponseMulti[PhoneCaseResponse],
        status_code=status.HTTP_200_OK,
    )
    async def list_phone_cases(self) -> ResponseMulti[PhoneCaseResponse]:
        results = await self.service.list_phone_cases()
        return ResponseMulti[PhoneCaseResponse](result=results)

    @phone_case_router.get(
        "/phone-cases/{phone_case_id}",
        response_model=Response[PhoneCaseResponse],
        status_code=status.HTTP_200_OK,
    )
    async def get_phone_case(self, phone_case_id: int) -> Response[PhoneCaseResponse]:
        result = await self.service.get_phone_case(phone_case_id)
        return Response[PhoneCaseResponse](result=result)

    @phone_case_router.put(
        "/phone-cases/{phone_case_id}",
        response_model=Response[PhoneCaseResponse],
        status_code=status.HTTP_200_OK,
    )
    async def update_phone_case(
        self, phone_case_id: int, payload: PhoneCaseUpdate
    ) -> Response[PhoneCaseResponse]:
        result = await self.service.update_phone_case(
            phone_case_id, payload.model_dump(exclude_unset=True)
        )
        return Response[PhoneCaseResponse](result=result)

    @phone_case_router.delete(
        "/phone-cases/{phone_case_id}",
        response_model=None,
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_phone_case(self, phone_case_id: int):
        await self.service.delete_phone_case(phone_case_id)
        return None

    @phone_case_router.post(
        "/phone-case-templates",
        response_model=Response[PhoneCaseTemplateResponse],
        status_code=status.HTTP_201_CREATED,
    )
    async def create_template(self, payload: PhoneCaseTemplateCreate) -> Response[PhoneCaseTemplateResponse]:
        result = await self.service.create_template(payload.model_dump())
        return Response[PhoneCaseTemplateResponse](result=result)

    @phone_case_router.get(
        "/phone-case-templates",
        response_model=ResponseMulti[PhoneCaseTemplateResponse],
        status_code=status.HTTP_200_OK,
    )
    async def list_templates(self) -> ResponseMulti[PhoneCaseTemplateResponse]:
        results = await self.service.list_templates()
        return ResponseMulti[PhoneCaseTemplateResponse](result=results)

    @phone_case_router.get(
        "/phone-case-templates/{template_id}",
        response_model=Response[PhoneCaseTemplateResponse],
        status_code=status.HTTP_200_OK,
    )
    async def get_template(self, template_id: int) -> Response[PhoneCaseTemplateResponse]:
        result = await self.service.get_template(template_id)
        return Response[PhoneCaseTemplateResponse](result=result)

    @phone_case_router.put(
        "/phone-case-templates/{template_id}",
        response_model=Response[PhoneCaseTemplateResponse],
        status_code=status.HTTP_200_OK,
    )
    async def update_template(
        self, template_id: int, payload: PhoneCaseTemplateUpdate
    ) -> Response[PhoneCaseTemplateResponse]:
        result = await self.service.update_template(
            template_id, payload.model_dump(exclude_unset=True)
        )
        return Response[PhoneCaseTemplateResponse](result=result)

    @phone_case_router.delete(
        "/phone-case-templates/{template_id}",
        response_model=None,
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_template(self, template_id: int):
        await self.service.delete_template(template_id)
        return None
