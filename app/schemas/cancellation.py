from datetime import datetime

from pydantic import BaseModel


class CancellationCreate(BaseModel):
    reason: str
    cancelled_by: str = "Customer"


class CancellationResponse(BaseModel):
    id: int
    order_id: int
    reason: str
    cancelled_by: str
    cancelled_at: datetime | None = None

    class Config:
        from_attributes = True