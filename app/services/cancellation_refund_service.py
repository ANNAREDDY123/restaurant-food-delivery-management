from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.payment import Payment
from app.models.cancellation import Cancellation
from app.models.refund import Refund


def cancel_order(
    db: Session,
    order_id: int,
    reason: str,
    cancelled_by: str = "Customer",
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

    if order.order_status == "Cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is already cancelled",
        )

    if order.order_status == "Delivered":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delivered orders cannot be cancelled",
        )

    existing_cancellation = (
        db.query(Cancellation)
        .filter(Cancellation.order_id == order_id)
        .first()
    )

    if existing_cancellation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cancellation record already exists",
        )

    cancellation = Cancellation(
        order_id=order_id,
        reason=reason,
        cancelled_by=cancelled_by,
    )

    order.order_status = "Cancelled"

    if order.delivery_partner_id:
        from app.models.delivery_partner import (
            DeliveryPartner,
        )

        partner = (
            db.query(DeliveryPartner)
            .filter(
                DeliveryPartner.id
                == order.delivery_partner_id
            )
            .first()
        )

        if partner:
            partner.availability_status = True

    db.add(cancellation)
    db.commit()
    db.refresh(cancellation)

    return cancellation


def process_refund(
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

    if order.order_status != "Cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only cancelled orders are eligible for refund",
        )

    payment = (
        db.query(Payment)
        .filter(Payment.order_id == order_id)
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found for this order",
        )

    if payment.payment_status != "Success":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only successful payments are eligible for refund",
        )

    existing_refund = (
        db.query(Refund)
        .filter(Refund.order_id == order_id)
        .first()
    )

    if existing_refund:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refund already exists for this order",
        )

    refund = Refund(
        order_id=order_id,
        payment_id=payment.id,
        refund_amount=payment.amount,
        refund_status="Success",
        reason="Order cancelled",
        processed_at=datetime.utcnow(),
    )

    payment.payment_status = "Refunded"
    order.payment_status = "Refunded"

    db.add(refund)
    db.commit()
    db.refresh(refund)

    return refund


def get_refund_by_order(
    db: Session,
    order_id: int,
):
    refund = (
        db.query(Refund)
        .filter(Refund.order_id == order_id)
        .first()
    )

    if not refund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refund not found",
        )

    return refund