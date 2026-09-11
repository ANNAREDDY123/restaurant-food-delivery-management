from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100,
    )

    role: str = Field(
        default="Customer",
    )


class UserLogin(BaseModel):
    email: EmailStr

    password: str


class UserResponse(BaseModel):
    id: int

    full_name: str

    email: EmailStr

    role: str

    is_active: bool

    created_at: datetime

    class Config:
        from_attributes = True