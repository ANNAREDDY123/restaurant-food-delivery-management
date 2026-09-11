from pydantic import BaseModel


class MostOrderedFoodResponse(BaseModel):
    name: str
    quantity: int


class RestaurantDashboardResponse(BaseModel):
    restaurant_id: int

    today_orders: int
    pending_orders: int
    completed_orders: int
    cancelled_orders: int

    today_revenue: float
    monthly_revenue: float

    most_ordered_food: MostOrderedFoodResponse | None = None

    average_rating: float
    total_customers: int