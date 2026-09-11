from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel


class OrderCreate(BaseModel):
    customer_id: int
    address_id: int
    coupon_code: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: int
    food_item_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    address_id: int

    subtotal: float
    delivery_fee: float
    discount: float
    tax: float
    total_amount: float

    order_status: str
    payment_status: str

    created_at: datetime | None = None

    items: list[OrderItemResponse]

    class Config:
        from_attributes = True

class OrderCancelResponse(BaseModel):
    id: int
    order_status: str
    message: str

from typing import Literal


class OrderStatusUpdate(BaseModel):
    order_status: Literal[
        "Pending",
        "Accepted",
        "Preparing",
        "Ready",
        "Picked Up",
        "Out for Delivery",
        "Delivered",
        "Cancelled",
    ]