from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    order_id: int

    payment_method: Literal[
        "Cash",
        "UPI",
        "Card",
        "Net Banking",
    ]

    transaction_id: str | None = None


class PaymentStatusUpdate(BaseModel):
    payment_status: Literal[
        "Success",
        "Failed",
    ]


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True