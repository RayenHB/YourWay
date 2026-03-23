from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Enum, ForeignKey, JSON, Text, Boolean,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from FastAPI_back.db.base import Base
from enum import Enum as PyEnum
from datetime import datetime


class OrderStatus(PyEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class PhoneModelTable(Base):
    __tablename__ = "phone_models"

    id = Column(Integer, primary_key=True, index=True)

    brand = Column(String(100), nullable=False)      # Apple, Samsung, etc.
    model_name = Column(String(100), nullable=False) # iPhone 16, S24 Ultra, etc.

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    phone_cases = relationship("orders_manager.models.PhoneCaseTable", back_populates="phone_model")


class PhoneCaseTypeTable(Base):
    __tablename__ = "phone_case_types"

    id = Column(Integer, primary_key=True, index=True)

    type_name = Column(String(100), nullable=False)  # Slim, MagSafe, etc.
    description = Column(Text, nullable=True)

    has_magsafe = Column(Boolean, default=False, nullable=False)
    is_double_layer = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    phone_cases = relationship("orders_manager.models.PhoneCaseTable", back_populates="case_type")


class PhoneCaseTable(Base):
    """
    A sellable variant = (phone model + case type).
    Example: (iPhone 16 Pro, MagSafe Slim)
    """
    __tablename__ = "phone_cases"
    __table_args__ = (
        UniqueConstraint("phone_model_id", "case_type_id", name="uq_phone_cases_model_type"),
    )

    id = Column(Integer, primary_key=True, index=True)

    phone_model_id = Column(Integer, ForeignKey("phone_models.id"), nullable=False)
    case_type_id = Column(Integer, ForeignKey("phone_case_types.id"), nullable=False)

    # optional commerce fields
    sku = Column(String(100), nullable=True, unique=True)
    price = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    phone_model = relationship("orders_manager.models.PhoneModelTable", back_populates="phone_cases")
    case_type = relationship("orders_manager.models.PhoneCaseTypeTable", back_populates="phone_cases")
    template = relationship("orders_manager.models.PhoneCaseTemplateTable", back_populates="phone_case", uselist=False)


class PhoneCaseTemplateTable(Base):
    """
    Template assets used by the editor and print export.
    Mask here = print area mask (usually includes bleed).
    """
    __tablename__ = "phone_case_templates"
    __table_args__ = (
        UniqueConstraint("phone_case_id", name="uq_phone_case_templates_phone_case_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    phone_case_id = Column(Integer, ForeignKey("phone_cases.id"), nullable=False)

    # Stored in Azure Blob; keep only URLs/keys in Postgres
    base_image_url = Column(String(500), nullable=False)       # preview base (webp/png)
    print_mask_url = Column(String(500), nullable=False)       # REQUIRED (png)
    overlay_image_url = Column(String(500), nullable=True)     # optional (png/webp)

    # Print/export sizing (authoritative)
    width_px = Column(Integer, nullable=False)   # e.g., 886
    height_px = Column(Integer, nullable=False)  # e.g., 1772
    dpi = Column(Integer, default=300, nullable=False)

    # Optional guides (for editor UI)
    bleed_mm = Column(Float, nullable=True)
    safe_mm = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    phone_case = relationship("orders_manager.models.PhoneCaseTable", back_populates="template")


class OrderTable(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False)

    # Link order to a specific sellable variant
    phone_case_id = Column(Integer, ForeignKey("phone_cases.id"), nullable=False)

    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)

    # User customization saved from the editor (layers, positions, fonts, image refs)
    customization_json = Column(JSON, nullable=True)

    # Generated outputs saved in Azure Blob
    preview_image_url = Column(String(500), nullable=True)  # low-res preview
    print_image_url = Column(String(500), nullable=True)    # high-res print file

    shipping_address = Column(Text, nullable=True)
    shipping_postal_code = Column(String(20), nullable=True)

    orderer_name = Column(String(100), nullable=False)
    orderer_email = Column(String(100), nullable=False)
    orderer_phone = Column(String(20), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    phone_case = relationship("orders_manager.models.PhoneCaseTable")

    @property
    def phone_model(self):
        return self.phone_case.phone_model if self.phone_case else None

    @property
    def case_type(self):
        return self.phone_case.case_type if self.phone_case else None

    @property
    def template(self):
        return self.phone_case.template if self.phone_case else None