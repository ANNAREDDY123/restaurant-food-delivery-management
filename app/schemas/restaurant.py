from datetime import time

from pydantic import BaseModel, Field


# ============================================================
# CREATE RESTAURANT
# ============================================================

class RestaurantCreate(BaseModel):
    restaurant_name: str = Field(
        min_length=2,
        max_length=150,
    )

    address: str = Field(
        min_length=5,
        max_length=255,
    )

    city: str = Field(
        min_length=2,
        max_length=100,
    )

    phone: str = Field(
        min_length=10,
        max_length=20,
    )

    cuisine_type: str = Field(
        min_length=2,
        max_length=100,
    )

    opening_time: time

    closing_time: time

    delivery_radius: float = Field(
        default=5.0,
        gt=0,
    )


# ============================================================
# UPDATE RESTAURANT
# ============================================================

class RestaurantUpdate(BaseModel):
    restaurant_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    address: str | None = Field(
        default=None,
        min_length=5,
        max_length=255,
    )

    city: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=20,
    )

    cuisine_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    opening_time: time | None = None

    closing_time: time | None = None

    status: str | None = None

    delivery_radius: float | None = Field(
        default=None,
        gt=0,
    )


# ============================================================
# RESTAURANT RESPONSE
# ============================================================

class RestaurantResponse(BaseModel):
    id: int
    restaurant_name: str
    owner_id: int
    address: str
    city: str
    phone: str
    cuisine_type: str
    opening_time: time
    closing_time: time
    status: str
    delivery_radius: float

    class Config:
        from_attributes = True