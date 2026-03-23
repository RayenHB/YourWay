from FastAPI_back.dependencies.service import get_service
from FastAPI_back.utils.response import Response, ResponseMulti
from fastapi import APIRouter, Depends, Query
from fastapi_utils.cbv import cbv
from orders_manager.OrderRepository import OrderRepository
from orders_manager.CaseRepository import CaseRepository
from phone_case_manager.CaseRepository import CaseRepository as UsedCaseRepository
from orders_manager.PhoneRepository import PhoneRepository
from orders_manager.PhoneCaseRepository import PhoneCaseRepository
from orders_manager.schemas import OrderResponse
from orders_manager.schemas import (
    OrderCreate,
    OrderResponse,
    OrderDetailResponse,
    OrderUpdate,
    OrderStatus,
    PhoneModelCreate,
    PhoneCaseTypeCreate,
    CreateOrderRequest,
    CreateOrderFromCaseRequest,
)
from orders_manager.Service import Service
from orders_manager.PhoneCaseTemplateRepository import PhoneCaseTemplateRepository
from admin_manager.dependencies import get_current_active_user
from admin_manager.schemas import AdminResponse





order_router = APIRouter(prefix="")

@cbv(order_router)
class OrderRouter:
    service: Service = Depends(
        get_service(
            Service,
            OrderRepository,
            PhoneRepository,
            CaseRepository,
            PhoneCaseRepository,
            PhoneCaseTemplateRepository,
            UsedCaseRepository,
        )
    )

    @order_router.post("/create-order", response_model=Response[OrderDetailResponse])
    async def create_order(
        self,
        request: CreateOrderRequest,
       
    ) -> Response[OrderDetailResponse]:
        result = await self.service.create_order(
            request.phone_payload.model_dump(),
            request.case_payload.model_dump(),
            request.phone_case_payload.model_dump(),
            request.template_payload.model_dump() if request.template_payload else None,
            request.order_payload.model_dump(),
        )
        return Response[OrderDetailResponse](result=result)

    @order_router.post("/create-order-from-case", response_model=Response[OrderDetailResponse])
    async def create_order_from_case(
        self,
        request: CreateOrderFromCaseRequest,
        
    ) -> Response[OrderDetailResponse]:
        result = await self.service.create_order_from_case(
            request.phone_case_id,
            request.order_payload.model_dump(),
        )
        return Response[OrderDetailResponse](result=result)
    
    @order_router.get("/orders", response_model=ResponseMulti[OrderDetailResponse])
    async def get_all_orders(
        self,
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=50, ge=1, le=200),
        current_user: AdminResponse = Depends(get_current_active_user)
    ) -> ResponseMulti[OrderDetailResponse]:
        results = await self.service.get_all_orders(page=page, page_size=page_size)
        return ResponseMulti[OrderDetailResponse](result=results)

    @order_router.get("/orders/{order_id}", response_model=Response[OrderDetailResponse])
    async def get_order_by_id(
        self,
        order_id: int,
        current_user: AdminResponse = Depends(get_current_active_user)

    ) -> Response[OrderDetailResponse]:
        result = await self.service.get_order_by_id(order_id)
        return Response[OrderDetailResponse](result=result)

    @order_router.get("/orders/find/{order_number}", response_model=Response[OrderDetailResponse])
    async def find_order(
        self,
        order_number: str,
        current_user: AdminResponse = Depends(get_current_active_user)
    ) -> Response[OrderDetailResponse]:
        result = await self.service.find_order(order_number)
        return Response[OrderDetailResponse](result=result)

    @order_router.get("/orders/search/{query}", response_model=ResponseMulti[OrderDetailResponse])
    async def search_orders(
        self,
        query: str,
        limit: int = Query(default=50, ge=1, le=200),
        current_user: AdminResponse = Depends(get_current_active_user)

    ) -> ResponseMulti[OrderDetailResponse]:
        results = await self.service.search_orders(query, limit=limit)
        return ResponseMulti[OrderDetailResponse](result=results)

    @order_router.put("/orders/{order_id}/complete", response_model=Response[OrderResponse])
    async def complete_order(
        self,
        order_id: int,
        current_user: AdminResponse = Depends(get_current_active_user)
    ) -> Response[OrderResponse]:
        result = await self.service.update_order_status(order_id, {"status": OrderStatus.COMPLETED})
        return Response[OrderResponse](result=result)

    @order_router.put("/orders/{order_id}/pending", response_model=Response[OrderResponse])
    async def pending_order(
        self,
        order_id: int,
        current_user: AdminResponse = Depends(get_current_active_user)
    ) -> Response[OrderResponse]:
        result = await self.service.update_order_status(order_id, {"status": OrderStatus.PENDING})
        return Response[OrderResponse](result=result)
        