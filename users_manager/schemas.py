from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field

from FastAPI_back.utils.entities import InternalEntity
from users_manager.models import UserRole, UserStatus

class _UserBase(InternalEntity):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=50)
    role: UserRole
    status: UserStatus

class UserFlat(_UserBase):
    id : int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUncommited(_UserBase):
    password: str = Field(..., min_length=8, max_length=128)
