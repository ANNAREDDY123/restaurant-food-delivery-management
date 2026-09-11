from app.models.restaurant import Restaurant
from app.models.food_item import FoodItem

from app.models.customer import Customer
from app.models.address import Address

from app.models.order import Order
from app.models.order_item import OrderItem

from app.models.payment import Payment
from app.models.cancellation import Cancellation
from app.models.refund import Refund


# ============================================================
# RESTAURANT -> FOOD ITEMS
# ============================================================

def test_restaurant_food_items_relationship():
    assert (
        Restaurant.food_items.property
        .mapper.class_
        == FoodItem
    )


# ============================================================
# CUSTOMER -> ADDRESSES
# ============================================================

def test_customer_addresses_relationship():
    assert (
        Customer.addresses.property
        .mapper.class_
        == Address
    )


# ============================================================
# ORDER -> ORDER ITEMS
# ============================================================

def test_order_items_relationship():
    assert (
        Order.items.property
        .mapper.class_
        == OrderItem
    )


# ============================================================
# ORDER -> PAYMENT
# ============================================================

def test_order_payment_relationship():
    assert (
        Order.payment.property
        .mapper.class_
        == Payment
    )


# ============================================================
# ORDER -> CANCELLATION
# ============================================================

def test_order_cancellation_relationship():
    assert (
        Order.cancellation.property
        .mapper.class_
        == Cancellation
    )


# ============================================================
# ORDER -> REFUND
# ============================================================

def test_order_refund_relationship():
    assert (
        Order.refund.property
        .mapper.class_
        == Refund
    )
from app.models.review import Review
from app.models.delivery_partner import DeliveryPartner


# ============================================================
# REVIEW -> CUSTOMER
# ============================================================

def test_review_customer_relationship():
    assert (
        Review.customer.property
        .mapper.class_
        == Customer
    )


# ============================================================
# REVIEW -> ORDER
# ============================================================

def test_review_order_relationship():
    assert (
        Review.order.property
        .mapper.class_
        == Order
    )


# ============================================================
# REVIEW -> RESTAURANT
# ============================================================

def test_review_restaurant_relationship():
    assert (
        Review.restaurant.property
        .mapper.class_
        == Restaurant
    )


# ============================================================
# REVIEW -> FOOD ITEM
# ============================================================

def test_review_food_item_relationship():
    assert (
        Review.food_item.property
        .mapper.class_
        == FoodItem
    )


# ============================================================
# REVIEW -> DELIVERY PARTNER
# ============================================================

def test_review_delivery_partner_relationship():
    assert (
        Review.delivery_partner.property
        .mapper.class_
        == DeliveryPartner
    )