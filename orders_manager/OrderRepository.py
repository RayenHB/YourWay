from typing import Any, Dict, List, Optional

from FastAPI_back.utils.repositories import BaseRepository
from orders_manager.models import OrderTable, PhoneCaseTable
from orders_manager.schemas import OrderCreate, OrderResponse, OrderDetailResponse
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload


DEFAULT_ORDER_PAGE_SIZE = 50
MAX_ORDER_PAGE_SIZE = 200
DEFAULT_SEARCH_LIMIT = 50
MAX_SEARCH_LIMIT = 200


def _order_relations():
    return (
        selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.phone_model),
        selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.case_type),
        selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.template),
    )


def _clamp_limit(value: int, default_value: int, max_value: int) -> int:
    if value is None:
        return default_value
    return max(1, min(int(value), max_value))



class OrderRepository(BaseRepository[OrderTable]):
    
    schema_class = OrderTable


    async def create(self, schema: OrderCreate) -> OrderDetailResponse:
        instance: OrderTable = await self._save(schema.model_dump())
        query = (
            select(OrderTable)
            .where(OrderTable.id == instance.id)
            .options(*_order_relations())
        )
        result = await self._session.execute(query)
        instance = result.scalars().one()
        return OrderDetailResponse.model_validate(instance)


    async def get_all_orders(
            self,
            page: int = 1,
            page_size: int = DEFAULT_ORDER_PAGE_SIZE,
    ) -> List[OrderDetailResponse]:
        page = max(int(page), 1)
        page_size = _clamp_limit(page_size, DEFAULT_ORDER_PAGE_SIZE, MAX_ORDER_PAGE_SIZE)
        offset = (page - 1) * page_size

        query = (
            select(OrderTable)
            .options(*_order_relations())
            .order_by(OrderTable.created_at.desc())
            .limit(page_size)
            .offset(offset)
        )
        result = await self._session.execute(query)
        instances = result.scalars().all()
        return [OrderDetailResponse.model_validate(instance) for instance in instances]

    async def get_by_id(self, order_id: int) -> Optional[OrderDetailResponse]:
        query = (
            select(OrderTable)
            .where(OrderTable.id == order_id)
            .options(*_order_relations())
        )
        result = await self._session.execute(query)
        instance = result.scalars().one_or_none()
        if not instance:
            return None
        return OrderDetailResponse.model_validate(instance)

    async def find_by_order_number(self, order_number: str) -> Optional[OrderDetailResponse]:
        query = (
            select(OrderTable)
            .where(OrderTable.order_number == order_number)
            .options(*_order_relations())
            .limit(1)
        )
        result = await self._session.execute(query)
        instance = result.scalars().one_or_none()
        if not instance:
            return None
        return OrderDetailResponse.model_validate(instance)

    async def search_by_query(self, query_text: str, limit: int = DEFAULT_SEARCH_LIMIT) -> List[OrderDetailResponse]:
        query_text = (query_text or "").strip()
        if not query_text:
            return []

        limit = _clamp_limit(limit, DEFAULT_SEARCH_LIMIT, MAX_SEARCH_LIMIT)

        query = (
            select(OrderTable)
            .where(
                or_(
                    OrderTable.order_number.ilike(f"%{query_text}%"),
                    OrderTable.orderer_name.ilike(f"%{query_text}%"),
                )
            )
            .options(*_order_relations())
            .order_by(OrderTable.created_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(query)
        instances = result.scalars().all()
        return [OrderDetailResponse.model_validate(instance) for instance in instances]

    async def update_status(self, order_id: int, payload) -> OrderResponse:
        instance = await self._update("id", order_id, payload)
        return OrderResponse.model_validate(instance)
        