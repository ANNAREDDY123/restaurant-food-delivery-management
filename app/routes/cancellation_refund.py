from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.cancellation import (
    CancellationCreate,
    CancellationResponse,
)

from app.schemas.refund import (
    RefundResponse,
)

from app.services.cancellation_refund_service import (
    cancel_order,
    process_refund,
    get_refund_by_order,
)

from app.services.notification_service import (
    notify_refund_processed,
)


router = APIRouter(
    tags=["Cancellation & Refund"],
)


# ============================================================
# CANCEL ORDER
# ============================================================

@router.post(
    "/orders/{order_id}/cancel",
    response_model=CancellationResponse,
    status_code=status.HTTP_201_CREATED,
)
def cancel_existing_order(
    order_id: int,
    cancellation_data: CancellationCreate,
    db: Session = Depends(get_db),
):
    return cancel_order(
        db=db,
        order_id=order_id,
        reason=cancellation_data.reason,
        cancelled_by=cancellation_data.cancelled_by,
    )


# ============================================================
# PROCESS REFUND
# ============================================================

@router.post(
    "/orders/{order_id}/refund",
    response_model=RefundResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_refund(
    order_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    refund = process_refund(
        db=db,
        order_id=order_id,
    )

    # Send refund processed notification
    background_tasks.add_task(
        notify_refund_processed,
        order_id,
        refund.refund_amount,
    )

    return refund


# ============================================================
# GET REFUND BY ORDER
# ============================================================

@router.get(
    "/orders/{order_id}/refund",
    response_model=RefundResponse,
)
def get_refund(
    order_id: int,
    db: Session = Depends(get_db),
):
    return get_refund_by_order(
        db=db,
        order_id=order_id,
    )