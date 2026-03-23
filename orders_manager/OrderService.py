from typing import Optional, List

from FastAPI_back.db.transactional import Transactional, Propagation
from orders_manager.OrderRepository import OrderRepository
from orders_manager.schemas import OrderCreate, OrderResponse, OrderUpdate, OrderStatus, OrderDetailResponse


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
    ):
        self.order_repository = order_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_order(
            self, payload: dict,
    ) -> OrderDetailResponse:
        order = OrderCreate(**payload)
        return await self.order_repository.create(order)


    async def get_all_orders(
            self,
            page: int = 1,
            page_size: int = 50,
    ) -> List[OrderDetailResponse]:
        return await self.order_repository.get_all_orders(page=page, page_size=page_size)

    async def get_order_by_id(self, order_id: int) -> Optional[OrderDetailResponse]:
        return await self.order_repository.get_by_id(order_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def find_order(self, order_number: str) -> Optional[OrderDetailResponse]:
        return await self.order_repository.find_by_order_number(order_number)

    @Transactional(propagation=Propagation.REQUIRED)
    async def search_orders(self, query_text: str, limit: int = 50) -> List[OrderDetailResponse]:
        return await self.order_repository.search_by_query(query_text, limit=limit)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_order_status(
            self,
            order_id: int,
            payload: dict,
    ) -> OrderResponse:
        return await self.order_repository.update_status(order_id, {"status": OrderStatus.COMPLETED})


    @Transactional(propagation=Propagation.REQUIRED)
    async def update_order_status_pending(
            self,
            order_id: int,
            payload: dict,
    ) -> OrderResponse:
        return await self.order_repository.update_status(order_id, {"status": OrderStatus.PENDING})


    

