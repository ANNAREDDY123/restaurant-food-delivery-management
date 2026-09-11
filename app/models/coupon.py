from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
)
from sqlalchemy.sql import func

from app.database import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    coupon_code = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    discount_type = Column(
        String,
        nullable=False,
    )

    discount_value = Column(
        Float,
        nullable=False,
    )

    minimum_order_value = Column(
        Float,
        nullable=False,
        default=0,
    )

    maximum_discount = Column(
        Float,
        nullable=True,
    )

    start_date = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    expiry_date = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    usage_limit = Column(
        Integer,
        nullable=True,
    )

    usage_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    status = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )