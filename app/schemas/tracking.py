from datetime import datetime

from pydantic import BaseModel


class TrackingCreate(BaseModel):
    status: str
    location: str | None = None
    remarks: str | None = None


class TrackingResponse(BaseModel):
    id: int
    order_id: int
    status: str
    location: str | None = None
    remarks: str | None = None
    timestamp: datetime

    class Config:
        from_attributes = True