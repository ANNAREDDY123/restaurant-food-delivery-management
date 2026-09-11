from datetime import datetime

from pydantic import BaseModel


class RefundResponse(BaseModel):
    id: int
    order_id: int
    payment_id: int | None = None
    refund_amount: float
    refund_status: str
    reason: str | None = None
    created_at: datetime | None = None
    processed_at: datetime | None = None

    class Config:
        from_attributes = True