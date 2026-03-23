from pydantic import Field
from typing import Optional
from datetime import datetime
from FastAPI_back.utils.entities import InternalEntity


class PhoneBase(InternalEntity):
    brand: str = Field(..., min_length=1, max_length=100)
    model_name: str = Field(..., min_length=1, max_length=100)


class PhoneCreate(PhoneBase):
    pass


class PhoneUpdate(InternalEntity):
    brand: Optional[str] = Field(None, max_length=100)
    model_name: Optional[str] = Field(None, max_length=100)


class PhoneResponse(PhoneBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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
    title: Optional[str] = Field(None, max_length=200)
    thumbnail_url: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, ge=0)
    active: bool = Field(default=True)


class PhoneCaseCreate(PhoneCaseBase):
    pass


class PhoneCaseUpdate(InternalEntity):
    phone_model_id: Optional[int] = None
    case_type_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=200)
    thumbnail_url: Optional[str] = Field(None, max_length=500)
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
    width_px: int = Field(..., gt=0)
    height_px: int = Field(..., gt=0)
    dpi: int = Field(300, gt=0)


class PhoneCaseTemplateCreate(PhoneCaseTemplateBase):
    pass


class PhoneCaseTemplateUpdate(InternalEntity):
    base_image_url: Optional[str] = Field(None, max_length=500)
    print_mask_url: Optional[str] = Field(None, max_length=500)
    overlay_image_url: Optional[str] = Field(None, max_length=500)
    width_px: Optional[int] = None
    height_px: Optional[int] = None
    dpi: Optional[int] = None


class PhoneCaseTemplateResponse(PhoneCaseTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreatePhoneWithCase(InternalEntity):
    phone_payload: PhoneCreate
    case_type_payload: PhoneCaseTypeCreate
    phone_case_payload: PhoneCaseCreate
    template_payload: Optional[PhoneCaseTemplateCreate] = None

class PhoneWithCaseResponse(InternalEntity):
    phone_model: PhoneResponse
    case_type: PhoneCaseTypeResponse
    phone_case: PhoneCaseResponse
    template: Optional[PhoneCaseTemplateResponse] = None
