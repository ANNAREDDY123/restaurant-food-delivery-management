from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.payment import (
    PaymentCreate,
    PaymentStatusUpdate,
    PaymentResponse,
)

from app.services.payment_service import (
    create_payment,
    get_payment_by_order,
    update_payment_status,
)

from app.services.notification_service import (
    notify_payment_success,
)


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


# ============================================================
# CREATE PAYMENT
# ============================================================

@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_payment(
    payment_data: PaymentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    payment = create_payment(
        db=db,
        order_id=payment_data.order_id,
        payment_method=payment_data.payment_method,
        transaction_id=payment_data.transaction_id,
    )

    # Send notification if payment is already successful
    if payment.payment_status == "Success":
        background_tasks.add_task(
            notify_payment_success,
            payment.order_id,
        )

    return payment


# ============================================================
# GET PAYMENT BY ORDER
# ============================================================

@router.get(
    "/{order_id}",
    response_model=PaymentResponse,
)
def get_payment(
    order_id: int,
    db: Session = Depends(get_db),
):
    return get_payment_by_order(
        db=db,
        order_id=order_id,
    )


# ============================================================
# UPDATE PAYMENT STATUS
# ============================================================

@router.patch(
    "/{payment_id}/status",
    response_model=PaymentResponse,
)
def update_status(
    payment_id: int,
    payment_data: PaymentStatusUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    payment = update_payment_status(
        db=db,
        payment_id=payment_id,
        payment_status=payment_data.payment_status,
    )

    # Send payment success notification
    if payment.payment_status == "Paid":
        background_tasks.add_task(
            notify_payment_success,
            payment.order_id,
        )

    return payment