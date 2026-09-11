from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class CouponCreate(BaseModel):
    coupon_code: str = Field(
        ...,
        min_length=3,
        max_length=50,
    )

    discount_type: Literal[
        "percentage",
        "fixed",
    ]

    discount_value: float = Field(
        ...,
        gt=0,
    )

    minimum_order_value: float = Field(
        default=0,
        ge=0,
    )

    maximum_discount: float | None = Field(
        default=None,
        gt=0,
    )

    start_date: datetime
    expiry_date: datetime

    usage_limit: int | None = Field(
        default=None,
        gt=0,
    )

    status: bool = True

    @model_validator(mode="after")
    def validate_dates(self):
        if self.expiry_date <= self.start_date:
            raise ValueError(
                "Expiry date must be after start date"
            )

        return self

    @model_validator(mode="after")
    def validate_discount(self):
        if (
            self.discount_type == "percentage"
            and self.discount_value > 100
        ):
            raise ValueError(
                "Percentage discount cannot be greater than 100"
            )

        return self


class CouponResponse(BaseModel):
    id: int
    coupon_code: str
    discount_type: str
    discount_value: float
    minimum_order_value: float
    maximum_discount: float | None
    start_date: datetime
    expiry_date: datetime
    usage_limit: int | None
    usage_count: int
    status: bool

    class Config:
        from_attributes = True


class CouponApply(BaseModel):
    coupon_code: str
    customer_id: int
    order_value: float = Field(
        ...,
        gt=0,
    )