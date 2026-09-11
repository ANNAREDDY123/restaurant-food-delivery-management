from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.address import Address
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.coupon import Coupon
from app.models.delivery_partner import DeliveryPartner
from app.models.food_item import FoodItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.restaurant import Restaurant


TAX_RATE = 0.05
DELIVERY_FEE = 40.0


def create_order(
    db: Session,
    customer_id: int,
    address_id: int,
    coupon_code: str | None = None,
):
    # ---------------------------------
    # Check cart
    # ---------------------------------

    cart = (
        db.query(Cart)
        .filter(Cart.customer_id == customer_id)
        .first()
    )

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found",
        )

    cart_items = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id)
        .all()
    )

    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty",
        )

    # ---------------------------------
    # Check restaurant
    # ---------------------------------

    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == cart.restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    if restaurant.status != "Open":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant is currently not accepting orders",
        )

    # ---------------------------------
    # Check address
    # ---------------------------------

    address = (
        db.query(Address)
        .filter(
            Address.id == address_id,
            Address.customer_id == customer_id,
        )
        .first()
    )

    if not address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid delivery address",
        )

    # ---------------------------------
    # Calculate subtotal
    # ---------------------------------

    subtotal = 0
    order_items_data = []

    for cart_item in cart_items:
        food_item = (
            db.query(FoodItem)
            .filter(
                FoodItem.id == cart_item.food_item_id
            )
            .first()
        )

        if not food_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Food item not found",
            )

        if not food_item.availability:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"{food_item.name} is currently unavailable"
                ),
            )

        item_total = (
            food_item.price
            * cart_item.quantity
        )

        subtotal += item_total

        order_items_data.append(
            {
                "food_item_id": food_item.id,
                "quantity": cart_item.quantity,
                "price": food_item.price,
            }
        )

    # ---------------------------------
    # Apply coupon
    # ---------------------------------

    discount = 0

    if coupon_code:
        coupon = (
            db.query(Coupon)
            .filter(
                Coupon.coupon_code
                == coupon_code.upper()
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

        if subtotal < coupon.minimum_order_value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum order value not satisfied",
            )

        if (
            coupon.usage_limit is not None
            and coupon.usage_count
            >= coupon.usage_limit
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon usage limit exceeded",
            )

        if coupon.discount_type == "percentage":
            discount = (
                subtotal
                * coupon.discount_value
                / 100
            )

            if (
                coupon.maximum_discount
                is not None
                and discount
                > coupon.maximum_discount
            ):
                discount = coupon.maximum_discount

        else:
            discount = coupon.discount_value

        if discount > subtotal:
            discount = subtotal

        # Increase usage only when order is created
        coupon.usage_count += 1

    # ---------------------------------
    # Calculate totals
    # ---------------------------------

    tax = subtotal * TAX_RATE

    total_amount = (
        subtotal
        + tax
        + DELIVERY_FEE
        - discount
    )

    # ---------------------------------
    # Create order
    # ---------------------------------

    try:
        order = Order(
            customer_id=customer_id,
            restaurant_id=restaurant.id,
            address_id=address.id,
            subtotal=subtotal,
            delivery_fee=DELIVERY_FEE,
            discount=discount,
            tax=tax,
            total_amount=total_amount,
            order_status="Pending",
            payment_status="Pending",
        )

        db.add(order)
        db.flush()

        # ---------------------------------
        # Create order items
        # ---------------------------------

        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                food_item_id=item_data[
                    "food_item_id"
                ],
                quantity=item_data["quantity"],
                price=item_data["price"],
            )

            db.add(order_item)

        # ---------------------------------
        # Clear cart
        # ---------------------------------

        (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart.id
            )
            .delete()
        )

        db.commit()

        db.refresh(order)

        return order

    except Exception:
        db.rollback()
        raise


def cancel_order(
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

    if order.order_status == "Cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is already cancelled",
        )

    restricted_statuses = [
        "Ready",
        "Picked Up",
        "Out for Delivery",
        "Delivered",
    ]

    if order.order_status in restricted_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Order cannot be cancelled when status is "
                f"'{order.order_status}'"
            ),
        )

    order.order_status = "Cancelled"

    db.commit()
    db.refresh(order)

    return order


def update_order_status(
    db: Session,
    order_id: int,
    new_status: str,
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
            detail="Cancelled order status cannot be changed",
        )

    if order.order_status == "Delivered":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delivered order status cannot be changed",
        )

    valid_transitions = {
        "Pending": [
            "Accepted",
            "Cancelled",
        ],
        "Accepted": [
            "Preparing",
            "Cancelled",
        ],
        "Preparing": [
            "Ready",
            "Cancelled",
        ],
        "Ready": [
            "Picked Up",
        ],
        "Picked Up": [
            "Out for Delivery",
        ],
        "Out for Delivery": [
            "Delivered",
        ],
    }

    allowed_statuses = valid_transitions.get(
        order.order_status,
        [],
    )

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Cannot change order status from "
                f"'{order.order_status}' to '{new_status}'"
            ),
        )

    order.order_status = new_status

    # ---------------------------------
    # Make delivery partner available
    # after successful delivery
    # ---------------------------------

    if (
        new_status == "Delivered"
        and order.delivery_partner_id is not None
    ):
        delivery_partner = (
            db.query(DeliveryPartner)
            .filter(
                DeliveryPartner.id
                == order.delivery_partner_id
            )
            .first()
        )

        if delivery_partner:
            delivery_partner.availability_status = True

    db.commit()
    db.refresh(order)

    return order