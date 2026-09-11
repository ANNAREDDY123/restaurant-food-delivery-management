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


class Address(Base):
    __tablename__ = "addresses"

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

    address_line = Column(
        String(255),
        nullable=False,
    )

    city = Column(
        String(100),
        nullable=False,
    )

    pincode = Column(
        String(20),
        nullable=False,
    )

    latitude = Column(
        Float,
        nullable=True,
    )

    longitude = Column(
        Float,
        nullable=True,
    )

    address_type = Column(
        String(50),
        nullable=False,
        default="Home",
    )

    is_default = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    customer = relationship(
        "Customer",
        back_populates="addresses",
    )