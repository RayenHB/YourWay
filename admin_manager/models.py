from sqlalchemy import Column,String,Enum
from FastAPI_back.db.base import Base
from enum import Enum as PyEnum

class UserRole(PyEnum):
    ADMIN = "ADMIN"

class AdminStatus(PyEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"



class UserTable(Base):
    __tablename__ = 'admins'
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.ADMIN)
    status = Column(Enum(AdminStatus), nullable=False, default=AdminStatus.ACTIVE)

