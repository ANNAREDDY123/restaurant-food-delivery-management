from pydantic import BaseModel


class TopRestaurantResponse(BaseModel):
    restaurant_id: int
    restaurant_name: str
    total_orders: int
    revenue: float


class TopFoodItemResponse(BaseModel):
    food_item_id: int
    food_item_name: str
    total_quantity: int


class PopularCuisineResponse(BaseModel):
    cuisine: str
    total_orders: int


class DailyOrdersResponse(BaseModel):
    date: str
    total_orders: int


class MonthlyRevenueResponse(BaseModel):
    month: str
    revenue: float


class AdminAnalyticsResponse(BaseModel):
    total_restaurants: int
    total_customers: int
    total_orders: int

    total_revenue: float
    total_refunds: float

    active_delivery_partners: int

    top_restaurants: list[TopRestaurantResponse]
    top_food_items: list[TopFoodItemResponse]

    most_popular_cuisine: PopularCuisineResponse | None = None

    daily_orders: list[DailyOrdersResponse]
    monthly_revenue: list[MonthlyRevenueResponse]

    cancellation_rate: float