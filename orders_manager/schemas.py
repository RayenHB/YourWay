from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
from FastAPI_back.utils.entities import InternalEntity






class OrderStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
  


# Phone Model Schemas
class PhoneModelBase(InternalEntity):
    brand: str = Field(..., min_length=1, max_length=100)
    model_name: str = Field(..., min_length=1, max_length=100)


class PhoneModelCreate(PhoneModelBase):
    pass


class PhoneModelUpdate(PhoneModelBase):
    brand: Optional[str] = Field(None, max_length=100)
    model_name: Optional[str] = Field(None, max_length=100)


class PhoneModelResponse(PhoneModelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Phone Case Type Schemas
class PhoneCaseTypeBase(InternalEntity):
    type_name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    has_magsafe: bool = Field(default=False)
    is_double_layer: bool = Field(default=False)


class PhoneCaseTypeCreate(PhoneCaseTypeBase):
    pass


class PhoneCaseTypeUpdate(InternalEntity):
    type_name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    has_magsafe: Optional[bool] = None
    is_double_layer: Optional[bool] = None


class PhoneCaseTypeResponse(PhoneCaseTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PhoneCaseBase(InternalEntity):
    phone_model_id: int
    case_type_id: int
    sku: Optional[str] = Field(None, max_length=100)
    price: Optional[float] = None


class PhoneCaseCreate(PhoneCaseBase):
    pass


class PhoneCaseUpdate(InternalEntity):
    phone_model_id: Optional[int] = None
    case_type_id: Optional[int] = None
    sku: Optional[str] = Field(None, max_length=100)
    price: Optional[float] = None
    active: Optional[bool] = None


class PhoneCaseResponse(PhoneCaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PhoneCaseTemplateBase(InternalEntity):
    phone_case_id: int
    base_image_url: str = Field(..., max_length=500)
    print_mask_url: str = Field(..., max_length=500)
    overlay_image_url: Optional[str] = Field(None, max_length=500)
    width_px: int
    height_px: int
    dpi: int = 300
    bleed_mm: Optional[float] = None
    safe_mm: Optional[float] = None


class PhoneCaseTemplateCreate(PhoneCaseTemplateBase):
    pass


class PhoneCaseTemplateUpdate(InternalEntity):
    base_image_url: Optional[str] = Field(None, max_length=500)
    print_mask_url: Optional[str] = Field(None, max_length=500)
    overlay_image_url: Optional[str] = Field(None, max_length=500)
    width_px: Optional[int] = None
    height_px: Optional[int] = None
    dpi: Optional[int] = None
    bleed_mm: Optional[float] = None
    safe_mm: Optional[float] = None


class PhoneCaseTemplateResponse(PhoneCaseTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderBase(InternalEntity):
    order_number: str = Field(..., min_length=1, max_length=50)
    orderer_name: str = Field(..., min_length=1, max_length=100)
    orderer_email: EmailStr
    orderer_phone: Optional[str] = Field(None, max_length=20)
    phone_case_id: int
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    customization_json: Optional[Dict[str, Any]] = None
    preview_image_url: Optional[str] = Field(None, max_length=500)
    print_image_url: Optional[str] = Field(None, max_length=500)
    shipping_address: Optional[str] = None


class OrderCreate(InternalEntity):
    order_number: Optional[str] = Field(None, max_length=50)
    orderer_name: str = Field(..., min_length=1, max_length=100)
    orderer_email: EmailStr
    orderer_phone: Optional[str] = Field(None, max_length=20)
    phone_case_id: Optional[int] = None
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    customization_json: Optional[Dict[str, Any]] = None
    preview_image_url: Optional[str] = Field(None, max_length=500)
    print_image_url: Optional[str] = Field(None, max_length=500)
    shipping_address: Optional[str] = None
    shipping_postal_code: Optional[str] = Field(None, max_length=20)


class OrderUpdate(BaseModel):
    orderer_name: Optional[str] = Field(None, max_length=100)
    orderer_email: Optional[EmailStr] = None
    orderer_phone: Optional[str] = Field(None, max_length=20)
    shipping_address: Optional[str] = None
    shipping_postal_code: Optional[str] = Field(None, max_length=20)
    status: Optional[OrderStatus] = None


class OrderResponse(OrderBase):
    id: int


    class Config:
        from_attributes = True


class OrderDetailResponse(OrderResponse):
    phone_model: PhoneModelResponse
    phone_case: PhoneCaseResponse
    case_type: PhoneCaseTypeResponse
    template: Optional[PhoneCaseTemplateResponse] = None



# Nested Response Schemas for API Endpoints
class PhoneModelDetailResponse(PhoneModelResponse):
    pass


class PhoneCaseTypeDetailResponse(PhoneCaseTypeResponse):
    pass



class CreateOrderRequest(InternalEntity):
    phone_payload: PhoneModelCreate
    case_payload: PhoneCaseTypeCreate
    phone_case_payload: PhoneCaseCreate
    template_payload: Optional[PhoneCaseTemplateCreate] = None
    order_payload: OrderCreate


class CreateOrderFromCaseRequest(InternalEntity):
    phone_case_id: int
    order_payload: OrderCreate