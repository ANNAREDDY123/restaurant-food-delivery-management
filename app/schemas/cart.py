from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    customer_id: int
    food_item_id: int
    quantity: int = Field(
        ...,
        gt=0,
    )


class CartItemUpdate(BaseModel):
    quantity: int = Field(
        ...,
        gt=0,
    )


class CartItemResponse(BaseModel):
    id: int
    food_item_id: int
    quantity: int

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    items: list[CartItemResponse]

    class Config:
        from_attributes = True