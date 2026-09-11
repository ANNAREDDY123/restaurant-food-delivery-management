from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Refund(Base):
    __tablename__ = "refunds"

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

    payment_id = Column(
        Integer,
        ForeignKey("payments.id"),
        nullable=True,
    )

    refund_amount = Column(
        Float,
        nullable=False,
    )

    refund_status = Column(
        String,
        nullable=False,
        default="Pending",
    )

    reason = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    processed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    order = relationship(
        "Order",
        back_populates="refund",
    )

    payment = relationship(
        "Payment",
        back_populates="refunds",
    )