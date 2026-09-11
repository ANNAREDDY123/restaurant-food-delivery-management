from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.customer import Customer
from app.models.food_item import FoodItem


def add_item_to_cart(
    db: Session,
    customer_id: int,
    food_item_id: int,
    quantity: int,
):
    # Check customer
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

    # Check food item
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

    # Check food availability
    if not food_item.availability:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Food item is currently unavailable",
        )

    # Find customer's cart
    cart = (
        db.query(Cart)
        .filter(Cart.customer_id == customer_id)
        .first()
    )

    # Create cart if it doesn't exist
    if not cart:
        cart = Cart(
            customer_id=customer_id,
            restaurant_id=food_item.restaurant_id,
        )

        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Cart can contain items from only one restaurant
    if cart.restaurant_id != food_item.restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Cart can contain items from only one restaurant. "
                "Please clear your cart before adding items from another restaurant."
            ),
        )

    # Check if item already exists in cart
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.food_item_id == food_item_id,
        )
        .first()
    )

    # Update quantity if item already exists
    if cart_item:
        cart_item.quantity += quantity

    else:
        cart_item = CartItem(
            cart_id=cart.id,
            food_item_id=food_item_id,
            quantity=quantity,
        )

        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart

def get_cart(
    db: Session,
    customer_id: int,
):
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

    items = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id)
        .all()
    )

    subtotal = 0

    for item in items:
        food_item = (
            db.query(FoodItem)
            .filter(FoodItem.id == item.food_item_id)
            .first()
        )

        if food_item:
            subtotal += food_item.price * item.quantity

    return {
        "cart": cart,
        "items": items,
        "subtotal": subtotal,
    }


def update_cart_item(
    db: Session,
    customer_id: int,
    item_id: int,
    quantity: int,
):
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

    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id,
        )
        .first()
    )

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found",
        )

    cart_item.quantity = quantity

    db.commit()
    db.refresh(cart_item)

    return cart_item


def remove_cart_item(
    db: Session,
    customer_id: int,
    item_id: int,
):
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

    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id,
        )
        .first()
    )

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found",
        )

    db.delete(cart_item)
    db.flush()

    remaining_items = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id)
        .count()
    )

    # Delete the cart if there are no items left.
    if remaining_items == 0:
        db.delete(cart)

    db.commit()

    return {
        "message": "Item removed from cart successfully"
    }

def clear_cart(
    db: Session,
    customer_id: int,
):
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

    (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id)
        .delete()
    )

    db.commit()

    return {
        "message": "Cart cleared successfully"
    }