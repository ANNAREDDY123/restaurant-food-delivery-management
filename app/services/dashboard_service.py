from datetime import datetime, time

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.food_item import FoodItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.restaurant import Restaurant
from app.models.review import Review


def get_restaurant_dashboard(
    db: Session,
    restaurant_id: int,
):
    # ========================================================
    # CHECK RESTAURANT
    # ========================================================

    restaurant = (
        db.query(Restaurant)
        .filter(
            Restaurant.id == restaurant_id
        )
        .first()
    )

    if not restaurant:
        return None

    # ========================================================
    # DATE RANGES
    # ========================================================

    now = datetime.now()

    today_start = datetime.combine(
        now.date(),
        time.min,
    )

    today_end = datetime.combine(
        now.date(),
        time.max,
    )

    month_start = datetime(
        now.year,
        now.month,
        1,
    )

    # ========================================================
    # TODAY'S ORDERS
    # ========================================================

    todays_orders = (
        db.query(Order)
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.created_at >= today_start,
            Order.created_at <= today_end,
        )
        .count()
    )

    # ========================================================
    # PENDING ORDERS
    # ========================================================

    pending_orders = (
        db.query(Order)
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.order_status == "Pending",
        )
        .count()
    )

    # ========================================================
    # COMPLETED ORDERS
    # ========================================================

    completed_orders = (
        db.query(Order)
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.order_status == "Delivered",
        )
        .count()
    )

    # ========================================================
    # CANCELLED ORDERS
    # ========================================================

    cancelled_orders = (
        db.query(Order)
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.order_status == "Cancelled",
        )
        .count()
    )

    # ========================================================
    # TODAY'S REVENUE
    # ========================================================

    todays_revenue = (
        db.query(
            func.coalesce(
                func.sum(Order.total_amount),
                0,
            )
        )
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.order_status == "Delivered",
            Order.created_at >= today_start,
            Order.created_at <= today_end,
        )
        .scalar()
    )

    # ========================================================
    # MONTHLY REVENUE
    # ========================================================

    monthly_revenue = (
        db.query(
            func.coalesce(
                func.sum(Order.total_amount),
                0,
            )
        )
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.order_status == "Delivered",
            Order.created_at >= month_start,
        )
        .scalar()
    )

    # ========================================================
    # MOST ORDERED FOOD
    # ========================================================

    most_ordered_food = (
        db.query(
            FoodItem.name.label(
                "food_name"
            ),
            func.sum(
                OrderItem.quantity
            ).label(
                "total_quantity"
            ),
        )
        .join(
            OrderItem,
            OrderItem.food_item_id
            == FoodItem.id,
        )
        .join(
            Order,
            Order.id
            == OrderItem.order_id,
        )
        .filter(
            Order.restaurant_id
            == restaurant_id,
        )
        .group_by(
            FoodItem.id,
            FoodItem.name,
        )
        .order_by(
            func.sum(
                OrderItem.quantity
            ).desc()
        )
        .first()
    )

    if most_ordered_food:
        most_ordered_food_data = {
            "name": most_ordered_food.food_name,
            "quantity": (
                most_ordered_food.total_quantity
            ),
        }
    else:
        most_ordered_food_data = None

    # ========================================================
    # AVERAGE RATING
    # ========================================================

    average_rating = (
        db.query(
            func.coalesce(
                func.avg(Review.rating),
                0,
            )
        )
        .filter(
            Review.restaurant_id
            == restaurant_id,
        )
        .scalar()
    )

    # ========================================================
    # TOTAL CUSTOMERS
    # ========================================================

    total_customers = (
        db.query(
            func.count(
                func.distinct(
                    Order.customer_id
                )
            )
        )
        .filter(
            Order.restaurant_id
            == restaurant_id,
        )
        .scalar()
    )

    # ========================================================
    # RETURN DASHBOARD DATA
    # ========================================================

    return {
        "restaurant_id": restaurant_id,
        "today_orders": todays_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "today_revenue": float(
            todays_revenue or 0
        ),
        "monthly_revenue": float(
            monthly_revenue or 0
        ),
        "most_ordered_food": (
            most_ordered_food_data
        ),
        "average_rating": round(
            float(average_rating or 0),
            2,
        ),
        "total_customers": (
            total_customers or 0
        ),
    }