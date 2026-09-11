from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DeliveryPartnerCreate(BaseModel):
    name: str
    phone: str
    vehicle_type: str
    vehicle_number: str
    current_location: Optional[str] = None


class DeliveryPartnerStatusUpdate(BaseModel):
    availability_status: bool
    current_location: Optional[str] = None


class DeliveryPartnerResponse(BaseModel):
    id: int
    name: str
    phone: str
    vehicle_type: str
    vehicle_number: str
    availability_status: bool
    current_location: Optional[str] = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class AssignDriverRequest(BaseModel):
    delivery_partner_id: int