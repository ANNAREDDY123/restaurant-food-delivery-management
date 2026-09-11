from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.coupon import Coupon


def create_coupon(
    db: Session,
    coupon_data,
):
    existing_coupon = (
        db.query(Coupon)
        .filter(
            Coupon.coupon_code
            == coupon_data.coupon_code.upper()
        )
        .first()
    )

    if existing_coupon:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon code already exists",
        )

    coupon = Coupon(
        coupon_code=coupon_data.coupon_code.upper(),
        discount_type=coupon_data.discount_type,
        discount_value=coupon_data.discount_value,
        minimum_order_value=coupon_data.minimum_order_value,
        maximum_discount=coupon_data.maximum_discount,
        start_date=coupon_data.start_date,
        expiry_date=coupon_data.expiry_date,
        usage_limit=coupon_data.usage_limit,
        status=coupon_data.status,
    )

    db.add(coupon)
    db.commit()
    db.refresh(coupon)

    return coupon


def get_coupons(
    db: Session,
):
    return (
        db.query(Coupon)
        .order_by(Coupon.id.desc())
        .all()
    )


def apply_coupon(
    db: Session,
    coupon_code: str,
    customer_id: int,
    order_value: float,
):
    coupon = (
        db.query(Coupon)
        .filter(
            Coupon.coupon_code == coupon_code.upper()
        )
        .first()
    )

    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found",
        )

    if not coupon.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon is inactive",
        )

    now = datetime.utcnow()

    if coupon.start_date > now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon is not active yet",
        )

    if coupon.expiry_date < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon has expired",
        )

    if order_value < coupon.minimum_order_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum order value not satisfied",
        )

    if (
        coupon.usage_limit is not None
        and coupon.usage_count >= coupon.usage_limit
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon usage limit exceeded",
        )

    # Calculate discount
    if coupon.discount_type == "percentage":
        discount = (
            order_value
            * coupon.discount_value
            / 100
        )

        if (
            coupon.maximum_discount is not None
            and discount > coupon.maximum_discount
        ):
            discount = coupon.maximum_discount

    else:
        discount = coupon.discount_value

    # Discount cannot be greater than order value
    if discount > order_value:
        discount = order_value

    # Increase coupon usage count
    coupon.usage_count += 1

    db.commit()
    db.refresh(coupon)

    return {
        "coupon_code": coupon.coupon_code,
        "order_value": order_value,
        "discount": discount,
        "final_amount": order_value - discount,
    }