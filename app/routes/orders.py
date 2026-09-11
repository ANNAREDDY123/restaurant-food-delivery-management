from datetime import datetime

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order

from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
)

from app.services.order_service import (
    create_order,
    update_order_status,
)

from app.services.notification_service import (
    notify_order_placed,
    notify_order_status_changed,
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


# ============================================================
# CREATE ORDER
# ============================================================

@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def place_order(
    order_data: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    order = create_order(
        db=db,
        customer_id=order_data.customer_id,
        address_id=order_data.address_id,
        coupon_code=order_data.coupon_code,
    )

    # Send notification in background
    background_tasks.add_task(
        notify_order_placed,
        order.id,
    )

    return order


# ============================================================
# GET ALL ORDERS
# SEARCH / FILTER / PAGINATION / SORTING
# ============================================================

@router.get(
    "",
    response_model=list[OrderResponse],
)
def get_all_orders(
    order_status: str | None = None,
    payment_status: str | None = None,
    restaurant_id: int | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "created_at",
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
            detail="Limit must be between 1 and 100",
        )

    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Start date cannot be greater "
                "than end date"
            ),
        )

    query = db.query(Order)

    # Filter by order status
    if order_status:
        query = query.filter(
            Order.order_status == order_status
        )

    # Filter by payment status
    if payment_status:
        query = query.filter(
            Order.payment_status == payment_status
        )

    # Filter by restaurant
    if restaurant_id is not None:
        query = query.filter(
            Order.restaurant_id == restaurant_id
        )

    # Filter by start date
    if start_date is not None:
        query = query.filter(
            Order.created_at >= start_date
        )

    # Filter by end date
    if end_date is not None:
        query = query.filter(
            Order.created_at <= end_date
        )

    # --------------------------------------------------------
    # SORTING
    # --------------------------------------------------------

    allowed_sort_fields = {
        "id": Order.id,
        "created_at": Order.created_at,
        "updated_at": Order.updated_at,
        "total_amount": Order.total_amount,
        "subtotal": Order.subtotal,
        "order_status": Order.order_status,
        "payment_status": Order.payment_status,
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

    orders = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return orders


# ============================================================
# GET ORDER BY ID
# ============================================================

@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
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

    return order


# ============================================================
# UPDATE ORDER STATUS
# ============================================================

@router.put(
    "/{order_id}/status",
    response_model=OrderResponse,
)
def update_existing_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    order = update_order_status(
        db=db,
        order_id=order_id,
        new_status=status_data.order_status,
    )

    # Send status notification in background
    background_tasks.add_task(
        notify_order_status_changed,
        order.id,
        order.order_status,
    )

    return order