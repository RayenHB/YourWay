from sqlalchemy import Column,String,Enum
from FastAPI_back.db.base import Base
from enum import Enum as PyEnum

class UserRole(PyEnum):
    SUPER_ADMIN = "SUPER_ADMIN"
    PLATEFORM_USER = "PLATEFORM_USER"
    ADMIN = "ADMIN"
class UserStatus(PyEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class UserTable(Base):
    __tablename__ = 'users'
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    phone_number = Column(String(50), nullable=True)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.INACTIVE)

