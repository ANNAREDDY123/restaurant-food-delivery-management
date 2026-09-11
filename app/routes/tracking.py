from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.tracking import (
    TrackingCreate,
    TrackingResponse,
)

from app.services.tracking_service import (
    create_tracking_record,
    get_order_tracking,
)


router = APIRouter(
    prefix="/orders",
    tags=["Order Tracking"],
)


# ---------------------------------
# Add Order Tracking Update
# ---------------------------------

@router.post(
    "/{order_id}/tracking",
    response_model=TrackingResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_tracking_update(
    order_id: int,
    tracking_data: TrackingCreate,
    db: Session = Depends(get_db),
):
    return create_tracking_record(
        db=db,
        order_id=order_id,
        tracking_status=tracking_data.status,
        location=tracking_data.location,
        remarks=tracking_data.remarks,
    )


# ---------------------------------
# Get Order Tracking History
# ---------------------------------

@router.get(
    "/{order_id}/tracking",
    response_model=list[TrackingResponse],
)
def get_tracking_history(
    order_id: int,
    db: Session = Depends(get_db),
):
    return get_order_tracking(
        db=db,
        order_id=order_id,
    )