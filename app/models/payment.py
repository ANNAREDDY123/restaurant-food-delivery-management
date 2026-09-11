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


class Payment(Base):
    __tablename__ = "payments"

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

    amount = Column(
        Float,
        nullable=False,
    )

    payment_method = Column(
        String,
        nullable=False,
    )

    payment_status = Column(
        String,
        nullable=False,
        default="Pending",
    )

    transaction_id = Column(
        String,
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

    order = relationship(
        "Order",
        back_populates="payment",
    )

    refunds = relationship(
        "Refund",
        back_populates="payment",
    )