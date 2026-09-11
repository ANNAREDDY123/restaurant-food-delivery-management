from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.food_item import FoodItem
from app.models.restaurant import Restaurant
from app.schemas.food_item import (
    FoodItemCreate,
    FoodItemUpdate,
    FoodItemResponse,
)


router = APIRouter(
    prefix="/menu",
    tags=["Menu"],
)


# ============================================================
# CREATE FOOD ITEM
# ============================================================

@router.post(
    "/items",
    response_model=FoodItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_food_item(
    food_item: FoodItemCreate,
    db: Session = Depends(get_db),
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == food_item.restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    new_food_item = FoodItem(
        **food_item.model_dump()
    )

    db.add(new_food_item)
    db.commit()
    db.refresh(new_food_item)

    return new_food_item


# ============================================================
# GET FOOD ITEMS
# SEARCH / FILTER / PAGINATION / SORTING
# ============================================================

@router.get(
    "/items",
    response_model=list[FoodItemResponse],
)
def get_food_items(
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    vegetarian: bool | None = None,
    spicy_level: int | None = None,
    availability: bool | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # VALIDATE PAGINATION
    # --------------------------------------------------------

    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be greater than 0",
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100",
        )

    # --------------------------------------------------------
    # VALIDATE PRICE RANGE
    # --------------------------------------------------------

    if min_price is not None and min_price < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum price cannot be negative",
        )

    if max_price is not None and max_price < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum price cannot be negative",
        )

    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Minimum price cannot be greater "
                "than maximum price"
            ),
        )

    query = db.query(FoodItem)

    # --------------------------------------------------------
    # FILTER BY CATEGORY
    # --------------------------------------------------------

    if category:
        query = query.filter(
            FoodItem.category.ilike(
                f"%{category}%"
            )
        )

    # --------------------------------------------------------
    # FILTER BY MINIMUM PRICE
    # --------------------------------------------------------

    if min_price is not None:
        query = query.filter(
            FoodItem.price >= min_price
        )

    # --------------------------------------------------------
    # FILTER BY MAXIMUM PRICE
    # --------------------------------------------------------

    if max_price is not None:
        query = query.filter(
            FoodItem.price <= max_price
        )

    # --------------------------------------------------------
    # FILTER BY VEGETARIAN
    # --------------------------------------------------------

    if vegetarian is not None:
        query = query.filter(
            FoodItem.vegetarian == vegetarian
        )

    # --------------------------------------------------------
    # FILTER BY SPICY LEVEL
    # --------------------------------------------------------

    if spicy_level is not None:
        query = query.filter(
            FoodItem.spicy_level == spicy_level
        )

    # --------------------------------------------------------
    # FILTER BY AVAILABILITY
    # --------------------------------------------------------

    if availability is not None:
        query = query.filter(
            FoodItem.availability == availability
        )

    # --------------------------------------------------------
    # SORTING
    # --------------------------------------------------------

    allowed_sort_fields = {
        "id": FoodItem.id,
        "name": FoodItem.name,
        "category": FoodItem.category,
        "price": FoodItem.price,
        "spicy_level": FoodItem.spicy_level,
        "preparation_time": FoodItem.preparation_time,
    }

    sort_column = allowed_sort_fields.get(
        sort_by
    )

    if not sort_column:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sort_by field",
        )

    if sort_order.lower() == "asc":
        query = query.order_by(
            sort_column.asc()
        )

    elif sort_order.lower() == "desc":
        query = query.order_by(
            sort_column.desc()
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "sort_order must be asc or desc"
            ),
        )

    # --------------------------------------------------------
    # PAGINATION
    # --------------------------------------------------------

    offset = (page - 1) * limit

    food_items = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return food_items


# ============================================================
# GET FOOD ITEM BY ID
# ============================================================

@router.get(
    "/items/{item_id}",
    response_model=FoodItemResponse,
)
def get_food_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    food_item = (
        db.query(FoodItem)
        .filter(FoodItem.id == item_id)
        .first()
    )

    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found",
        )

    return food_item


# ============================================================
# UPDATE FOOD ITEM
# ============================================================

@router.put(
    "/items/{item_id}",
    response_model=FoodItemResponse,
)
def update_food_item(
    item_id: int,
    food_item_data: FoodItemUpdate,
    db: Session = Depends(get_db),
):
    food_item = (
        db.query(FoodItem)
        .filter(FoodItem.id == item_id)
        .first()
    )

    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found",
        )

    update_data = food_item_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            food_item,
            field,
            value,
        )

    db.commit()
    db.refresh(food_item)

    return food_item


# ============================================================
# DELETE FOOD ITEM
# ============================================================

@router.delete(
    "/items/{item_id}",
)
def delete_food_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    food_item = (
        db.query(FoodItem)
        .filter(FoodItem.id == item_id)
        .first()
    )

    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found",
        )

    db.delete(food_item)
    db.commit()

    return {
        "message": "Food item deleted successfully"
    }