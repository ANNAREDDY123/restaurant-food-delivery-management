from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.sql import func

from app.database import Base


class DeliveryPartner(Base):
    __tablename__ = "delivery_partners"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(150),
        nullable=False,
    )

    phone = Column(
        String(20),
        unique=True,
        nullable=False,
    )

    vehicle_type = Column(
        String(50),
        nullable=False,
    )

    vehicle_number = Column(
        String(50),
        unique=True,
        nullable=False,
    )

    availability_status = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    current_location = Column(
        String(255),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )