from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.review import (
    ReviewCreate,
    ReviewResponse,
)

from app.services.review_service import (
    create_review,
    get_restaurant_reviews,
    get_food_item_reviews,
)


router = APIRouter(
    prefix="",
    tags=["Reviews"],
)


@router.post(
    "/reviews",
    response_model=ReviewResponse,
)
def add_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
):
    return create_review(
        db=db,
        customer_id=review_data.customer_id,
        order_id=review_data.order_id,
        restaurant_id=review_data.restaurant_id,
        food_item_id=review_data.food_item_id,
        delivery_partner_id=(
            review_data.delivery_partner_id
        ),
        rating=review_data.rating,
        review=review_data.review,
    )


@router.get(
    "/restaurants/{restaurant_id}/reviews",
    response_model=list[ReviewResponse],
)
def get_reviews_for_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    return get_restaurant_reviews(
        db=db,
        restaurant_id=restaurant_id,
    )


@router.get(
    "/food-items/{food_item_id}/reviews",
    response_model=list[ReviewResponse],
)
def get_reviews_for_food_item(
    food_item_id: int,
    db: Session = Depends(get_db),
):
    return get_food_item_reviews(
        db=db,
        food_item_id=food_item_id,
    )