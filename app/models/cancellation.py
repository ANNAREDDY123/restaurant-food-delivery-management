from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Cancellation(Base):
    __tablename__ = "cancellations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
        unique=True,
    )

    reason = Column(
        String,
        nullable=False,
    )

    cancelled_by = Column(
        String,
        nullable=False,
        default="Customer",
    )

    cancelled_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    order = relationship(
        "Order",
        back_populates="cancellation",
    )