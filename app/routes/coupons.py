from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.coupon import (
    CouponCreate,
    CouponResponse,
    CouponApply,
)
from app.services.coupon_service import (
    create_coupon,
    get_coupons,
    apply_coupon,
)


router = APIRouter(
    prefix="/coupons",
    tags=["Coupons"],
)


# ---------------------------------
# Create Coupon
# ---------------------------------

@router.post(
    "",
    response_model=CouponResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_coupon(
    coupon_data: CouponCreate,
    db: Session = Depends(get_db),
):
    return create_coupon(
        db=db,
        coupon_data=coupon_data,
    )


# ---------------------------------
# Get All Coupons
# ---------------------------------

@router.get(
    "",
    response_model=list[CouponResponse],
)
def get_all_coupons(
    db: Session = Depends(get_db),
):
    return get_coupons(
        db=db,
    )


# ---------------------------------
# Apply Coupon
# ---------------------------------

@router.post("/apply")
def apply_coupon_to_order(
    coupon_data: CouponApply,
    db: Session = Depends(get_db),
):
    return apply_coupon(
        db=db,
        coupon_code=coupon_data.coupon_code,
        customer_id=coupon_data.customer_id,
        order_value=coupon_data.order_value,
    )