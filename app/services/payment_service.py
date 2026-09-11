from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.payment import Payment


# ============================================================
# CREATE PAYMENT
# ============================================================

def create_payment(
    db: Session,
    order_id: int,
    payment_method: str,
    transaction_id: str | None = None,
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

    existing_payment = (
        db.query(Payment)
        .filter(Payment.order_id == order_id)
        .first()
    )

    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already exists for this order",
        )

    payment = Payment(
        order_id=order_id,
        amount=order.total_amount,
        payment_method=payment_method,
        payment_status="Pending",
        transaction_id=transaction_id,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


# ============================================================
# GET PAYMENT BY ORDER
# ============================================================

def get_payment_by_order(
    db: Session,
    order_id: int,
):
    payment = (
        db.query(Payment)
        .filter(Payment.order_id == order_id)
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    return payment


# ============================================================
# UPDATE PAYMENT STATUS
# ============================================================

def update_payment_status(
    db: Session,
    payment_id: int,
    payment_status: str,
):
    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id)
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    payment.payment_status = payment_status

    if payment_status == "Success":
        payment.order.payment_status = "Paid"

    elif payment_status == "Failed":
        payment.order.payment_status = "Failed"

    db.commit()
    db.refresh(payment)

    return payment