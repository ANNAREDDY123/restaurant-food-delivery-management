from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Float,
    Time,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    restaurant_name = Column(
        String(150),
        nullable=False,
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    address = Column(
        String(255),
        nullable=False,
    )

    city = Column(
        String(100),
        nullable=False,
        index=True,
    )

    phone = Column(
        String(20),
        nullable=False,
    )

    cuisine_type = Column(
        String(100),
        nullable=False,
        index=True,
    )

    opening_time = Column(
        Time,
        nullable=False,
    )

    closing_time = Column(
        Time,
        nullable=False,
    )

    status = Column(
        String(50),
        default="Open",
        nullable=False,
    )

    delivery_radius = Column(
        Float,
        default=5.0,
        nullable=False,
    )

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    owner = relationship(
        "User",
        back_populates="restaurants",
    )

    food_items = relationship(
        "FoodItem",
        back_populates="restaurant",
        cascade="all, delete-orphan",
    )