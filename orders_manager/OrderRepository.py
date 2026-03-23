from typing import Any, Dict, List, Optional

from FastAPI_back.utils.repositories import BaseRepository
from orders_manager.models import OrderTable, PhoneCaseTable
from orders_manager.schemas import OrderCreate, OrderResponse, OrderDetailResponse
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload



class OrderRepository(BaseRepository[OrderTable]):
    
    schema_class = OrderTable


    async def create(self, schema: OrderCreate) -> OrderDetailResponse:
        instance: OrderTable = await self._save(schema.model_dump())
        query = (
            select(OrderTable)
            .where(OrderTable.id == instance.id)
            .options(
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.phone_model),
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.case_type),
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.template),
            )
        )
        result = await self._session.execute(query)
        instance = result.scalars().one()
        return OrderDetailResponse.model_validate(instance)


    async def get_all_orders(
            self,
    ) -> List[OrderDetailResponse]:
        query = (
            select(OrderTable)
            .options(
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.phone_model),
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.case_type),
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.template),
            )
            .order_by(OrderTable.created_at.desc())
        )
        result = await self._session.execute(query)
        instances = result.scalars().all()
        return [OrderDetailResponse.model_validate(instance) for instance in instances]

    async def get_by_id(self, order_id: int) -> Optional[OrderDetailResponse]:
        query = (
            select(OrderTable)
            .where(OrderTable.id == order_id)
            .options(
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.phone_model),
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.case_type),
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.template),
            )
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
            .options(
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.phone_model),
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.case_type),
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.template),
            )
            .limit(1)
        )
        result = await self._session.execute(query)
        instance = result.scalars().one_or_none()
        if not instance:
            return None
        return OrderDetailResponse.model_validate(instance)

    async def search_by_query(self, query_text: str) -> List[OrderDetailResponse]:
        query = (
            select(OrderTable)
            .where(
                or_(
                    OrderTable.order_number.ilike(f"%{query_text}%"),
                    OrderTable.orderer_name.ilike(f"%{query_text}%"),
                )
            )
            .options(
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.phone_model),
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.case_type),
                selectinload(OrderTable.phone_case).selectinload(PhoneCaseTable.template),
            )
            .order_by(OrderTable.created_at.desc())
        )
        result = await self._session.execute(query)
        instances = result.scalars().all()
        return [OrderDetailResponse.model_validate(instance) for instance in instances]

    async def update_status(self, order_id: int, payload) -> OrderResponse:
        instance = await self._update("id", order_id, payload)
        return OrderResponse.model_validate(instance)
        