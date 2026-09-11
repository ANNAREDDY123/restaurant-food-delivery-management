from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False,
    )

    category = Column(
        String(100),
        nullable=False,
    )

    name = Column(
        String(150),
        nullable=False,
    )

    description = Column(
        String(500),
        nullable=True,
    )

    price = Column(
        Float,
        nullable=False,
    )

    preparation_time = Column(
        Integer,
        nullable=False,
    )

    availability = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    vegetarian = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    spicy_level = Column(
        Integer,
        default=0,
        nullable=False,
    )

    restaurant = relationship(
        "Restaurant",
        back_populates="food_items",
    )