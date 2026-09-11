from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartResponse,
)
from app.services.cart_service import (
    add_item_to_cart,
    get_cart,
    update_cart_item,
    remove_cart_item,
    clear_cart,
)


router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


# ---------------------------------
# Add Item to Cart
# ---------------------------------

@router.post(
    "/items",
    response_model=CartResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_cart_item(
    data: CartItemCreate,
    db: Session = Depends(get_db),
):
    return add_item_to_cart(
        db=db,
        customer_id=data.customer_id,
        food_item_id=data.food_item_id,
        quantity=data.quantity,
    )


# ---------------------------------
# Get Cart
# ---------------------------------

@router.get(
    "",
    response_model=CartResponse,
)
def view_cart(
    customer_id: int,
    db: Session = Depends(get_db),
):
    result = get_cart(
        db=db,
        customer_id=customer_id,
    )

    return result["cart"]


# ---------------------------------
# Update Cart Item
# ---------------------------------

@router.put(
    "/items/{item_id}",
)
def update_item(
    item_id: int,
    data: CartItemUpdate,
    customer_id: int,
    db: Session = Depends(get_db),
):
    return update_cart_item(
        db=db,
        customer_id=customer_id,
        item_id=item_id,
        quantity=data.quantity,
    )


# ---------------------------------
# Remove Cart Item
# ---------------------------------

@router.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    customer_id: int,
    db: Session = Depends(get_db),
):
    return remove_cart_item(
        db=db,
        customer_id=customer_id,
        item_id=item_id,
    )


# ---------------------------------
# Clear Cart
# ---------------------------------

@router.delete("/clear")
def empty_cart(
    customer_id: int,
    db: Session = Depends(get_db),
):
    return clear_cart(
        db=db,
        customer_id=customer_id,
    )