from datetime import datetime
from typing import Optional

from pydantic import Field, EmailStr

from users_manager.models import UserStatus, UserRole
from FastAPI_back.utils.entities import PublicEntity


class _UserBase(PublicEntity):
    name: str = Field(..., description="User's name")
    email: EmailStr = Field(..., description="User's email")
    phone_number: str = Field(..., description="User's number")
    status: UserStatus
    role: UserRole

class UserPublic(_UserBase):
    id : int
    created_at: Optional[datetime] = Field(alias="createdAt", default=None)
    updated_at: Optional[datetime] = Field(alias="updatedAt", default=None)
class UserCreateRequestBody(_UserBase):
    password: str = Field(..., description="User's password", min_length=8, max_length=128)


class UserUpdateRequestBody(_UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, description="User's password", min_length=8, max_length=128)
    status: Optional[UserStatus] = None
