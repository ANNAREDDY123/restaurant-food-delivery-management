from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.restaurant import Restaurant
from app.models.user import User
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
)
from app.routes.auth import get_current_user


router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
)


# ============================================================
# CREATE RESTAURANT
# ============================================================

@router.post(
    "",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_restaurant(
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if current_user.role not in [
        "Admin",
        "Restaurant Owner",
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Only Admin or Restaurant Owner "
                "can create restaurants"
            ),
        )

    if (
        restaurant_data.opening_time
        >= restaurant_data.closing_time
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Opening time must be before closing time"
            ),
        )

    new_restaurant = Restaurant(
        restaurant_name=restaurant_data.restaurant_name,
        owner_id=current_user.id,
        address=restaurant_data.address,
        city=restaurant_data.city,
        phone=restaurant_data.phone,
        cuisine_type=restaurant_data.cuisine_type,
        opening_time=restaurant_data.opening_time,
        closing_time=restaurant_data.closing_time,
        delivery_radius=restaurant_data.delivery_radius,
        status="Open",
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


# ============================================================
# GET ALL RESTAURANTS
# SEARCH / FILTER / PAGINATION / SORTING
# ============================================================

@router.get(
    "",
    response_model=list[RestaurantResponse],
)
def get_restaurants(
    cuisine: str | None = None,
    city: str | None = None,
    restaurant_status: str | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
):

    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be greater than 0",
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Limit must be between 1 and 100"
            ),
        )

    # Only show non-deleted restaurants
    query = (
        db.query(Restaurant)
        .filter(Restaurant.is_deleted == False)
    )

    # --------------------------------------------------------
    # FILTER BY CUISINE
    # --------------------------------------------------------

    if cuisine:
        query = query.filter(
            Restaurant.cuisine_type.ilike(
                f"%{cuisine}%"
            )
        )

    # --------------------------------------------------------
    # FILTER BY CITY
    # --------------------------------------------------------

    if city:
        query = query.filter(
            Restaurant.city.ilike(
                f"%{city}%"
            )
        )

    # --------------------------------------------------------
    # FILTER BY STATUS
    # --------------------------------------------------------

    if restaurant_status:
        query = query.filter(
            Restaurant.status == restaurant_status
        )

    # --------------------------------------------------------
    # SORTING
    # --------------------------------------------------------

    allowed_sort_fields = {
        "id": Restaurant.id,
        "restaurant_name": (
            Restaurant.restaurant_name
        ),
        "city": Restaurant.city,
        "cuisine_type": Restaurant.cuisine_type,
        "status": Restaurant.status,
    }

    sort_column = allowed_sort_fields.get(
        sort_by
    )

    if not sort_column:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid sort_by field"
            ),
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

    offset = (
        page - 1
    ) * limit

    restaurants = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return restaurants


# ============================================================
# GET RESTAURANT BY ID
# ============================================================

@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    restaurant = (
        db.query(Restaurant)
        .filter(
            Restaurant.id == restaurant_id,
            Restaurant.is_deleted == False,
        )
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    return restaurant


# ============================================================
# UPDATE RESTAURANT
# ============================================================

@router.put(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = (
        db.query(Restaurant)
        .filter(
            Restaurant.id == restaurant_id,
            Restaurant.is_deleted == False,
        )
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    if (
        current_user.role != "Admin"
        and restaurant.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You are not authorized to update "
                "this restaurant"
            ),
        )

    update_data = restaurant_data.model_dump(
        exclude_unset=True
    )

    new_opening_time = update_data.get(
        "opening_time",
        restaurant.opening_time,
    )

    new_closing_time = update_data.get(
        "closing_time",
        restaurant.closing_time,
    )

    if new_opening_time >= new_closing_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Opening time must be before closing time"
            ),
        )

    for field, value in update_data.items():
        setattr(
            restaurant,
            field,
            value,
        )

    db.commit()
    db.refresh(restaurant)

    return restaurant


# ============================================================
# DELETE RESTAURANT
# SOFT DELETE
# ============================================================

@router.delete(
    "/{restaurant_id}",
)
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = (
        db.query(Restaurant)
        .filter(
            Restaurant.id == restaurant_id,
            Restaurant.is_deleted == False,
        )
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    if (
        current_user.role != "Admin"
        and restaurant.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You are not authorized to delete "
                "this restaurant"
            ),
        )

    # Soft delete
    restaurant.is_deleted = True
    restaurant.deleted_at = datetime.utcnow()

    db.commit()

    return {
        "message": (
            "Restaurant deleted successfully"
        )
    }