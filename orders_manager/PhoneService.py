from typing import Any, Dict, List, Optional

from FastAPI_back.db.transactional import Transactional, Propagation
from orders_manager.PhoneRepository import PhoneRepository
from orders_manager.models import PhoneModelTable
from orders_manager.schemas import PhoneModelCreate, PhoneModelResponse


class PhoneService:
    def __init__(
        self,
        phone_repository: PhoneRepository,
    ):
        self.phone_repository = phone_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_phone_model(self, payload: dict) -> PhoneModelResponse:
        """Create a new phone model (not per order)"""
        result: PhoneModelCreate = PhoneModelCreate(**payload)
        return await self.phone_repository.create(result)

    