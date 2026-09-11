from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.review import Review
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.customer import Customer
from app.models.restaurant import Restaurant
from app.models.food_item import FoodItem
from app.models.delivery_partner import DeliveryPartner


# ============================================================
# CREATE REVIEW
# ============================================================

def create_review(
    db: Session,
    customer_id: int,
    order_id: int,
    rating: int,
    review: str | None = None,
    restaurant_id: int | None = None,
    food_item_id: int | None = None,
    delivery_partner_id: int | None = None,
):

    # --------------------------------------------------------
    # CHECK CUSTOMER
    # --------------------------------------------------------

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    # --------------------------------------------------------
    # CHECK ORDER
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # CUSTOMER MUST OWN THE ORDER
    # --------------------------------------------------------

    if order.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Customer can only review their own order"
            ),
        )

    # --------------------------------------------------------
    # ONLY DELIVERED ORDERS CAN BE REVIEWED
    # --------------------------------------------------------

    if order.order_status != "Delivered":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only delivered orders can be reviewed"
            ),
        )

    # --------------------------------------------------------
    # AT LEAST ONE REVIEW TARGET REQUIRED
    # --------------------------------------------------------

    if not any(
        [
            restaurant_id,
            food_item_id,
            delivery_partner_id,
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "At least one review target is required"
            ),
        )

    # ========================================================
    # RESTAURANT REVIEW VALIDATION
    # ========================================================

    if restaurant_id:

        restaurant = (
            db.query(Restaurant)
            .filter(
                Restaurant.id == restaurant_id
            )
            .first()
        )

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )

        # Restaurant must belong to the order
        if restaurant_id != order.restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Restaurant does not belong to this order"
                ),
            )

        # Prevent duplicate restaurant review
        existing_review = (
            db.query(Review)
            .filter(
                Review.customer_id == customer_id,
                Review.order_id == order_id,
                Review.restaurant_id == restaurant_id,
            )
            .first()
        )

        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Restaurant has already been reviewed "
                    "for this order"
                ),
            )

    # ========================================================
    # FOOD ITEM REVIEW VALIDATION
    # ========================================================

    if food_item_id:

        food_item = (
            db.query(FoodItem)
            .filter(
                FoodItem.id == food_item_id
            )
            .first()
        )

        if not food_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Food item not found",
            )

        # ----------------------------------------------------
        # IMPORTANT:
        # FOOD ITEM MUST BELONG TO THIS ORDER
        # ----------------------------------------------------

        order_item = (
            db.query(OrderItem)
            .filter(
                OrderItem.order_id == order_id,
                OrderItem.food_item_id == food_item_id,
            )
            .first()
        )

        if not order_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Food item does not belong to this order"
                ),
            )

        # Prevent duplicate food item review
        existing_review = (
            db.query(Review)
            .filter(
                Review.customer_id == customer_id,
                Review.order_id == order_id,
                Review.food_item_id == food_item_id,
            )
            .first()
        )

        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Food item has already been reviewed "
                    "for this order"
                ),
            )

    # ========================================================
    # DELIVERY PARTNER REVIEW VALIDATION
    # ========================================================

    if delivery_partner_id:

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

        # Delivery partner must belong to the order
        if (
            order.delivery_partner_id
            != delivery_partner_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Delivery partner does not belong "
                    "to this order"
                ),
            )

        # Prevent duplicate delivery partner review
        existing_review = (
            db.query(Review)
            .filter(
                Review.customer_id == customer_id,
                Review.order_id == order_id,
                Review.delivery_partner_id
                == delivery_partner_id,
            )
            .first()
        )

        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Delivery partner has already been "
                    "reviewed for this order"
                ),
            )

    # ========================================================
    # CREATE REVIEW
    # ========================================================

    new_review = Review(
        customer_id=customer_id,
        order_id=order_id,
        restaurant_id=restaurant_id,
        food_item_id=food_item_id,
        delivery_partner_id=delivery_partner_id,
        rating=rating,
        review=review,
    )

    try:

        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        return new_review

    except Exception:

        db.rollback()
        raise


# ============================================================
# GET RESTAURANT REVIEWS
# ============================================================

def get_restaurant_reviews(
    db: Session,
    restaurant_id: int,
):

    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    return (
        db.query(Review)
        .filter(
            Review.restaurant_id == restaurant_id
        )
        .order_by(
            Review.created_at.desc()
        )
        .all()
    )


# ============================================================
# GET FOOD ITEM REVIEWS
# ============================================================

def get_food_item_reviews(
    db: Session,
    food_item_id: int,
):

    food_item = (
        db.query(FoodItem)
        .filter(FoodItem.id == food_item_id)
        .first()
    )

    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found",
        )

    return (
        db.query(Review)
        .filter(
            Review.food_item_id == food_item_id
        )
        .order_by(
            Review.created_at.desc()
        )
        .all()
    )