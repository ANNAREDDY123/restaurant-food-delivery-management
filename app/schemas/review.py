from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    customer_id: int
    order_id: int

    restaurant_id: int | None = None
    food_item_id: int | None = None
    delivery_partner_id: int | None = None

    rating: int = Field(
        ...,
        ge=1,
        le=5,
    )

    review: str | None = None


class ReviewResponse(BaseModel):
    id: int
    customer_id: int
    order_id: int

    restaurant_id: int | None = None
    food_item_id: int | None = None
    delivery_partner_id: int | None = None

    rating: int
    review: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True