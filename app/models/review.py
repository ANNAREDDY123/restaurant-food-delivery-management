from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

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

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=True,
    )

    food_item_id = Column(
        Integer,
        ForeignKey("food_items.id"),
        nullable=True,
    )

    delivery_partner_id = Column(
        Integer,
        ForeignKey("delivery_partners.id"),
        nullable=True,
    )

    rating = Column(
        Integer,
        nullable=False,
    )

    review = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    customer = relationship(
        "Customer",
    )

    order = relationship(
        "Order",
    )

    restaurant = relationship(
        "Restaurant",
    )

    food_item = relationship(
        "FoodItem",
    )

    delivery_partner = relationship(
        "DeliveryPartner",
    )