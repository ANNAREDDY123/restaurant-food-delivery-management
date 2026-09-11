from datetime import datetime, time

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.delivery_partner import DeliveryPartner
from app.models.food_item import FoodItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.refund import Refund
from app.models.restaurant import Restaurant


def get_admin_analytics(
    db: Session,
):
    # ========================================================
    # BASIC TOTALS
    # ========================================================

    total_restaurants = (
        db.query(Restaurant)
        .count()
    )

    total_customers = (
        db.query(Customer)
        .count()
    )

    total_orders = (
        db.query(Order)
        .count()
    )

    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(Order.total_amount),
                0,
            )
        )
        .filter(
            Order.order_status == "Delivered"
        )
        .scalar()
    )

    total_refunds = (
        db.query(
            func.coalesce(
                func.sum(
                    Refund.refund_amount
                ),
                0,
            )
        )
        .scalar()
    )

    active_delivery_partners = (
        db.query(DeliveryPartner)
        .filter(
            DeliveryPartner.availability_status
            == True
        )
        .count()
    )

    # ========================================================
    # TOP RESTAURANTS
    # ========================================================

    top_restaurants_query = (
        db.query(
            Restaurant.id,
            Restaurant.restaurant_name,
            func.count(Order.id).label(
                "total_orders"
            ),
            func.coalesce(
                func.sum(
                    Order.total_amount
                ),
                0,
            ).label(
                "revenue"
            ),
        )
        .outerjoin(
            Order,
            Order.restaurant_id
            == Restaurant.id,
        )
        .group_by(
            Restaurant.id,
            Restaurant.restaurant_name,
        )
        .order_by(
            func.count(
                Order.id
            ).desc()
        )
        .limit(5)
        .all()
    )

    top_restaurants = [
        {
            "restaurant_id": restaurant.id,
            "restaurant_name": (
                restaurant.restaurant_name
            ),
            "total_orders": (
                restaurant.total_orders
            ),
            "revenue": float(
                restaurant.revenue or 0
            ),
        }
        for restaurant
        in top_restaurants_query
    ]

    # ========================================================
    # TOP FOOD ITEMS
    # ========================================================

    top_food_items_query = (
        db.query(
            FoodItem.id,
            FoodItem.name,
            func.coalesce(
                func.sum(
                    OrderItem.quantity
                ),
                0,
            ).label(
                "total_quantity"
            ),
        )
        .outerjoin(
            OrderItem,
            OrderItem.food_item_id
            == FoodItem.id,
        )
        .group_by(
            FoodItem.id,
            FoodItem.name,
        )
        .order_by(
            func.coalesce(
                func.sum(
                    OrderItem.quantity
                ),
                0,
            ).desc()
        )
        .limit(5)
        .all()
    )

    top_food_items = [
        {
            "food_item_id": food.id,
            "food_item_name": food.name,
            "total_quantity": (
                food.total_quantity
            ),
        }
        for food
        in top_food_items_query
    ]

    # ========================================================
    # MOST POPULAR CUISINE
    # ========================================================

    most_popular_cuisine = (
        db.query(
            Restaurant.cuisine_type,
            func.count(Order.id).label(
                "total_orders"
            ),
        )
        .join(
            Order,
            Order.restaurant_id
            == Restaurant.id,
        )
        .group_by(
            Restaurant.cuisine_type
        )
        .order_by(
            func.count(
                Order.id
            ).desc()
        )
        .first()
    )

    if most_popular_cuisine:
        popular_cuisine_data = {
            "cuisine": (
                most_popular_cuisine.cuisine_type
            ),
            "total_orders": (
                most_popular_cuisine.total_orders
            ),
        }
    else:
        popular_cuisine_data = None

    # ========================================================
    # DAILY ORDERS
    # ========================================================

    daily_orders_query = (
        db.query(
            func.date(
                Order.created_at
            ).label("date"),
            func.count(
                Order.id
            ).label("total_orders"),
        )
        .group_by(
            func.date(
                Order.created_at
            )
        )
        .order_by(
            func.date(
                Order.created_at
            ).desc()
        )
        .limit(30)
        .all()
    )

    daily_orders = [
        {
            "date": str(day.date),
            "total_orders": (
                day.total_orders
            ),
        }
        for day
        in daily_orders_query
    ]

    # ========================================================
    # MONTHLY REVENUE
    # ========================================================

    monthly_revenue_query = (
        db.query(
            func.strftime(
                "%Y-%m",
                Order.created_at,
            ).label("month"),
            func.coalesce(
                func.sum(
                    Order.total_amount
                ),
                0,
            ).label("revenue"),
        )
        .filter(
            Order.order_status
            == "Delivered"
        )
        .group_by(
            func.strftime(
                "%Y-%m",
                Order.created_at,
            )
        )
        .order_by(
            func.strftime(
                "%Y-%m",
                Order.created_at,
            ).desc()
        )
        .limit(12)
        .all()
    )

    monthly_revenue = [
        {
            "month": month.month,
            "revenue": float(
                month.revenue or 0
            ),
        }
        for month
        in monthly_revenue_query
    ]

    # ========================================================
    # CANCELLATION RATE
    # ========================================================

    cancelled_orders = (
        db.query(Order)
        .filter(
            Order.order_status
            == "Cancelled"
        )
        .count()
    )

    if total_orders > 0:
        cancellation_rate = round(
            (
                cancelled_orders
                / total_orders
            )
            * 100,
            2,
        )
    else:
        cancellation_rate = 0

    # ========================================================
    # RETURN ANALYTICS
    # ========================================================

    return {
        "total_restaurants": (
            total_restaurants
        ),
        "total_customers": (
            total_customers
        ),
        "total_orders": (
            total_orders
        ),
        "total_revenue": float(
            total_revenue or 0
        ),
        "total_refunds": float(
            total_refunds or 0
        ),
        "active_delivery_partners": (
            active_delivery_partners
        ),
        "top_restaurants": (
            top_restaurants
        ),
        "top_food_items": (
            top_food_items
        ),
        "most_popular_cuisine": (
            popular_cuisine_data
        ),
        "daily_orders": (
            daily_orders
        ),
        "monthly_revenue": (
            monthly_revenue
        ),
        "cancellation_rate": (
            cancellation_rate
        ),
    }