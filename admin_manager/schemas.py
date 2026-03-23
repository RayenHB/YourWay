from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field

from FastAPI_back.utils.entities import InternalEntity
from admin_manager.models import UserRole
from admin_manager.models import AdminStatus

class AdminBase(InternalEntity):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole
    status: AdminStatus

class AdminResponse(AdminBase):
    id : int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AdminCreate(AdminBase):
    password: str = Field(..., min_length=8, max_length=128)


class AdminLogin(InternalEntity):
    name: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)


class Token(InternalEntity): #
    access_token: str
    token_type: str


class TokenData(InternalEntity):
    sub: str | None = None