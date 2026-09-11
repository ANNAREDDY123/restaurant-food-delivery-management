from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_tracking import OrderTracking


def create_tracking_record(
    db: Session,
    order_id: int,
    tracking_status: str,
    location: str | None = None,
    remarks: str | None = None,
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    if order.order_status in [
        "Delivered",
        "Cancelled",
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Completed or cancelled orders cannot "
                "receive tracking updates"
            ),
        )

    tracking = OrderTracking(
        order_id=order_id,
        status=tracking_status,
        location=location,
        remarks=remarks,
    )

    db.add(tracking)

    # Update the actual order status
    order.order_status = tracking_status

    db.commit()

    db.refresh(tracking)
    db.refresh(order)

    return tracking


def get_order_tracking(
    db: Session,
    order_id: int,
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    tracking_history = (
        db.query(OrderTracking)
        .filter(
            OrderTracking.order_id == order_id
        )
        .order_by(
            OrderTracking.timestamp.asc()
        )
        .all()
    )

    return tracking_history