from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.delivery_partner import DeliveryPartner
from app.models.order import Order


ACTIVE_DELIVERY_STATUSES = [
    "Picked Up",
    "Out for Delivery",
]


def create_delivery_partner(
    db: Session,
    partner_data,
):
    existing_phone = (
        db.query(DeliveryPartner)
        .filter(
            DeliveryPartner.phone
            == partner_data.phone
        )
        .first()
    )

    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delivery partner phone already exists",
        )

    existing_vehicle = (
        db.query(DeliveryPartner)
        .filter(
            DeliveryPartner.vehicle_number
            == partner_data.vehicle_number
        )
        .first()
    )

    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle number already exists",
        )

    delivery_partner = DeliveryPartner(
        name=partner_data.name,
        phone=partner_data.phone,
        vehicle_type=partner_data.vehicle_type,
        vehicle_number=partner_data.vehicle_number,
        current_location=partner_data.current_location,
        availability_status=True,
    )

    db.add(delivery_partner)
    db.commit()
    db.refresh(delivery_partner)

    return delivery_partner


def get_delivery_partners(
    db: Session,
):
    return (
        db.query(DeliveryPartner)
        .order_by(
            DeliveryPartner.created_at.desc()
        )
        .all()
    )


def update_delivery_partner_status(
    db: Session,
    delivery_partner_id: int,
    availability_status: bool,
    current_location: str | None = None,
):
    delivery_partner = (
        db.query(DeliveryPartner)
        .filter(
            DeliveryPartner.id
            == delivery_partner_id
        )
        .first()
    )

    if not delivery_partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery partner not found",
        )

    delivery_partner.availability_status = (
        availability_status
    )

    if current_location is not None:
        delivery_partner.current_location = (
            current_location
        )

    db.commit()
    db.refresh(delivery_partner)

    return delivery_partner


def assign_driver_to_order(
    db: Session,
    order_id: int,
    delivery_partner_id: int,
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
        "Cancelled",
        "Delivered",
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Driver cannot be assigned to this order",
        )

    delivery_partner = (
        db.query(DeliveryPartner)
        .filter(
            DeliveryPartner.id
            == delivery_partner_id
        )
        .first()
    )

    if not delivery_partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery partner not found",
        )

    if not delivery_partner.availability_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delivery partner is not available",
        )

    active_order = (
        db.query(Order)
        .filter(
            Order.delivery_partner_id
            == delivery_partner_id,
            Order.order_status.in_(
                ACTIVE_DELIVERY_STATUSES
            ),
        )
        .first()
    )

    if active_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Delivery partner already has an active delivery"
            ),
        )

    order.delivery_partner_id = delivery_partner_id

    delivery_partner.availability_status = False

    db.commit()
    db.refresh(order)

    return order