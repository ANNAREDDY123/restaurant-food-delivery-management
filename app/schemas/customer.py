from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ============================================================
# CUSTOMER SCHEMAS
# ============================================================

class CustomerCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    phone: str = Field(
        min_length=10,
        max_length=20,
    )


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    email: Optional[EmailStr] = None

    phone: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=20,
    )


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# ADDRESS SCHEMAS
# ============================================================

class AddressCreate(BaseModel):
    address_line: str = Field(
        min_length=5,
        max_length=255,
    )

    city: str = Field(
        min_length=2,
        max_length=100,
    )

    pincode: str = Field(
        min_length=4,
        max_length=20,
    )

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    address_type: str = Field(
        default="Home",
        max_length=50,
    )

    is_default: bool = False


class AddressUpdate(BaseModel):
    address_line: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=255,
    )

    city: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    pincode: Optional[str] = Field(
        default=None,
        min_length=4,
        max_length=20,
    )

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    address_type: Optional[str] = Field(
        default=None,
        max_length=50,
    )

    is_default: Optional[bool] = None


class AddressResponse(BaseModel):
    id: int
    customer_id: int
    address_line: str
    city: str
    pincode: str
    latitude: Optional[float]
    longitude: Optional[float]
    address_type: str
    is_default: bool

    model_config = ConfigDict(
        from_attributes=True
    )