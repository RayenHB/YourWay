from sqlalchemy import (
    Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean, UniqueConstraint
)
from sqlalchemy.orm import relationship
from FastAPI_back.db.base import Base
from datetime import datetime


class PhoneModelTable(Base):
    __tablename__ = "used_phone_models"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), nullable=False)
    model_name = Column(String(100), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    phone_cases = relationship("phone_case_manager.models.PhoneCaseTable", back_populates="phone_model")


class PhoneCaseTypeTable(Base):
    __tablename__ = "used_phone_case_types"

    id = Column(Integer, primary_key=True, index=True)

    type_name = Column(String(100), nullable=False) 
    description = Column(Text, nullable=True)

    has_magsafe = Column(Boolean, default=False, nullable=False)
    is_double_layer = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    phone_cases = relationship("phone_case_manager.models.PhoneCaseTable", back_populates="case_type")


class PhoneCaseTable(Base):
    """
    Variant shown to user to choose & customize:
    (phone_model_id + case_type_id)
    """
    __tablename__ = "used_phone_cases"
    __table_args__ = (
        UniqueConstraint("phone_model_id", "case_type_id", name="uq_used_phone_cases_model_type"),
    )

    id = Column(Integer, primary_key=True, index=True)

    phone_model_id = Column(Integer, ForeignKey("used_phone_models.id"), nullable=False)
    case_type_id = Column(Integer, ForeignKey("used_phone_case_types.id"), nullable=False)

    # what you show in listing
    title = Column(String(200), nullable=True)     # "iPhone 16 Pro - MagSafe Case"
    thumbnail_url = Column(String(500), nullable=True)  # listing image (not necessarily base editor image)
    price = Column(Float, nullable=True)
    active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    phone_model = relationship("phone_case_manager.models.PhoneModelTable", back_populates="phone_cases")
    case_type = relationship("phone_case_manager.models.PhoneCaseTypeTable", back_populates="phone_cases")
    template = relationship("phone_case_manager.models.PhoneCaseTemplateTable", back_populates="phone_case", uselist=False)


class PhoneCaseTemplateTable(Base):
    """
    Assets for the customizer (base/mask/overlay).
    """
    __tablename__ = "used_phone_case_templates"
    __table_args__ = (
        UniqueConstraint("phone_case_id", name="uq_phone_case_templates_case_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    phone_case_id = Column(Integer, ForeignKey("used_phone_cases.id"), nullable=False)

    base_image_url = Column(String(500), nullable=False)    # blank case editor base
    print_mask_url = Column(String(500), nullable=False)    # mask with bleed (png)
    overlay_image_url = Column(String(500), nullable=True)  # optional

    width_px = Column(Integer, nullable=False)
    height_px = Column(Integer, nullable=False)
    dpi = Column(Integer, nullable=False, default=300)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    phone_case = relationship("phone_case_manager.models.PhoneCaseTable", back_populates="template")