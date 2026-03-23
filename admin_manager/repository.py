import logging
from typing import Optional

from sqlalchemy import func, select

from admin_manager.models import UserTable as Admins
from admin_manager.schemas import AdminResponse
from FastAPI_back.utils.repositories import BaseRepository




class AdminRepository(BaseRepository[Admins]):
    
    schema_class = Admins

    async def get_admin_by_name(self, name: str) -> Optional[Admins]:
        name_normalized = name.strip().lower()
        query = select(Admins).where(func.lower(Admins.name) == name_normalized).limit(1)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def get_admin_by_email(self, email: str) -> Optional[Admins]:
        email_normalized = email.strip().lower()
        query = select(Admins).where(func.lower(Admins.email) == email_normalized).limit(1)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def create_admin(self, admin_data: dict) -> AdminResponse:
        instance = await self._save(admin_data)
        return AdminResponse.model_validate(instance)

    async def count_admins(self) -> int:
        query = select(func.count()).select_from(Admins)
        result = await self._session.execute(query)
        return int(result.scalar_one() or 0)