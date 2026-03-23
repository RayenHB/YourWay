from typing import List, Optional
from FastAPI_back.db.transactional import Transactional, Propagation
from orders_manager.PhoneService import PhoneService
from orders_manager.CaseService import CaseService
from phone_case_manager.CaseService import CaseService as UsedCaseService
from orders_manager.PhoneCaseService import PhoneCaseService
from orders_manager.PhoneCaseTemplateService import PhoneCaseTemplateService
from orders_manager.OrderService import OrderService
from orders_manager.schemas import (
    PhoneModelCreate,
    PhoneCaseTypeCreate,
    OrderCreate,
    OrderResponse,
    OrderDetailResponse,
    OrderStatus,
    PhoneCaseCreate,
    PhoneCaseResponse,
    PhoneCaseTemplateCreate,
)
from orders_manager.OrderRepository import OrderRepository
from orders_manager.PhoneRepository import PhoneRepository
from orders_manager.CaseRepository import CaseRepository
from orders_manager.PhoneCaseRepository import PhoneCaseRepository
from orders_manager.PhoneCaseTemplateRepository import PhoneCaseTemplateRepository
from datetime import datetime
import uuid

from FastAPI_back.utils.errors import BadRequestError, NotFoundError
from orders_manager.helpers import is_valid_uae_postal_code, is_valid_uae_phone_number, send_email, send_notification



class Service:
    """Service for managing orders with phone models and case types"""

    def __init__(
           self,
        order_repository: OrderRepository,
        phone_repository: PhoneRepository,
        case_repository: CaseRepository,
        phone_case_repository: PhoneCaseRepository,
        phone_case_template_repository: PhoneCaseTemplateRepository,
        used_case_repository,
    ):
        self.order_service = OrderService(order_repository)
        self.phone_service = PhoneService(phone_repository)
        self.case_service = CaseService(case_repository)
        self.phone_case_service = PhoneCaseService(phone_case_repository)
        self.phone_case_template_service = PhoneCaseTemplateService(phone_case_template_repository)
        self.used_case_service = UsedCaseService(used_case_repository)

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_order(
        self,
        phone_payload: PhoneModelCreate,
        case_payload: PhoneCaseTypeCreate,
        phone_case_payload: PhoneCaseCreate,
        template_payload: Optional[PhoneCaseTemplateCreate],
        order_payload: OrderCreate,
    ) -> OrderDetailResponse:
        """Create order with phone model and case type"""
        
        # Create phone model first
        phone = await self.phone_service.create_phone_model(phone_payload)
        if not phone:
            raise NotFoundError(message="Failed to create phone model")

        # Capture used case type id before we overwrite payload
        used_case_type_id = phone_case_payload.get("case_type_id")

        # Create case type
        case_type = await self.case_service.create_case_type(case_payload)
        if not case_type:
            raise NotFoundError(message="Failed to create case type")

        # Create sellable variant (phone_case)
        phone_case_payload["phone_model_id"] = phone.id
        phone_case_payload["case_type_id"] = case_type.id

        if case_payload.get("has_magsafe") and used_case_type_id:
            await self.used_case_service.update_case_type(
                used_case_type_id,
                {"has_magsafe": True},
            )

        
        phone_case = await self.phone_case_service.create_phone_case(phone_case_payload)
        if not phone_case:
            raise NotFoundError(message="Failed to create phone case variant")

        if template_payload:
            template_payload["phone_case_id"] = phone_case.id

            template = await self.phone_case_template_service.create_template(template_payload)
            if not template:
                raise NotFoundError(message="Failed to create phone case template")

        # Update order payload with created phone_case_id
        order_payload['phone_case_id'] = phone_case.id
        if order_payload.get("orderer_email"):
            order_payload["orderer_email"] = str(order_payload["orderer_email"]).strip().lower()
        # Generate a unique order number using timestamp + uuid
        order_payload['order_number'] = f"ORD{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"

        # Validate UAE postal code if provided
        

        postal = order_payload.get('shipping_postal_code')
        if not is_valid_uae_postal_code(postal):
            raise BadRequestError(message="Invalid UAE postal code. Must be a 5-digit code.")

        

        phone = order_payload.get('orderer_phone')
        if not is_valid_uae_phone_number(phone):
            raise BadRequestError(message="Invalid UAE phone number.")

        send_email(order_payload)
        send_notification(order_payload)
        # Create order with the created phone and case IDs
        return await self.order_service.create_order(order_payload)

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_order_from_case(
        self,
        phone_case_id: int,
        order_payload: OrderCreate,
    ) -> OrderDetailResponse:
        phone_case = await self.phone_case_service.get_phone_case(phone_case_id)
        if not phone_case:
            raise NotFoundError(message="Phone case not found")

        order_payload["phone_case_id"] = phone_case.id
        if order_payload.get("orderer_email"):
            order_payload["orderer_email"] = str(order_payload["orderer_email"]).strip().lower()

        order_payload["order_number"] = (
            f"ORD{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
        )

        postal = order_payload.get("shipping_postal_code")
        if not is_valid_uae_postal_code(postal):
            raise BadRequestError(message="Invalid UAE postal code. Must be a 5-digit code.")

        phone = order_payload.get("orderer_phone")
        if not is_valid_uae_phone_number(phone):
            raise BadRequestError(message="Invalid UAE phone number.")

        send_email(order_payload)
        send_notification(order_payload)
        return await self.order_service.create_order(order_payload)

    @Transactional(propagation=Propagation.REQUIRED)
    async def get_all_orders(
        self,
        page: int = 1,
        page_size: int = 50,
    ) -> List[OrderResponse]:
        """Retrieve all orders with their phone models and case types"""
        return await self.order_service.get_all_orders(page=page, page_size=page_size)

    @Transactional(propagation=Propagation.REQUIRED)
    async def get_order_by_id(self, order_id: int) -> Optional[OrderDetailResponse]:
        """Retrieve a specific order by its ID"""
        return await self.order_service.get_order_by_id(order_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def find_order(self, order_number: str) -> Optional[OrderDetailResponse]:
        """Find an order by its order number"""
        return await self.order_service.find_order(order_number)

    @Transactional(propagation=Propagation.REQUIRED)
    async def search_orders(self, query_text: str, limit: int = 50) -> List[OrderDetailResponse]:
        """Search orders by order number or orderer name"""
        return await self.order_service.search_orders(query_text=query_text, limit=limit)


    @Transactional(propagation=Propagation.REQUIRED)
    async def update_order_status(
        self,
        order_id: int,
        payload: dict,
    ) -> OrderResponse:
        """Update the status of an existing order"""
        order = await self.order_service.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found.")

        order_dict = order.model_dump()

        if payload.get("status") == OrderStatus.PENDING:
            return await self.order_service.update_order_status_pending(order_id, order_dict)
        else:
            return await self.order_service.update_order_status(order_id, order_dict)


