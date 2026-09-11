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


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False,
    )

    address_id = Column(
        Integer,
        ForeignKey("addresses.id"),
        nullable=False,
    )

    delivery_partner_id = Column(
        Integer,
        ForeignKey("delivery_partners.id"),
        nullable=True,
    )

    subtotal = Column(
        Float,
        nullable=False,
    )

    delivery_fee = Column(
        Float,
        nullable=False,
        default=0,
    )

    discount = Column(
        Float,
        nullable=False,
        default=0,
    )

    tax = Column(
        Float,
        nullable=False,
        default=0,
    )

    total_amount = Column(
        Float,
        nullable=False,
    )

    order_status = Column(
        String,
        nullable=False,
        default="Pending",
    )

    payment_status = Column(
        String,
        nullable=False,
        default="Pending",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    tracking_history = relationship(
        "OrderTracking",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan",
    )

    cancellation = relationship(
        "Cancellation",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan",
    )

    refund = relationship(
        "Refund",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan",
    )