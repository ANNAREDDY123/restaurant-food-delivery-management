from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


# ============================================================
# USER REGISTER
# ============================================================

class UserRegister(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    password: str = Field(
        min_length=6,
        max_length=100,
    )

    role: str = Field(
        default="Customer",
    )


# ============================================================
# USER LOGIN
# ============================================================

class UserLogin(BaseModel):
    email: EmailStr

    password: str


# ============================================================
# REFRESH TOKEN
# ============================================================

class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ============================================================
# CHANGE PASSWORD
# ============================================================

class ChangePasswordRequest(BaseModel):
    old_password: str

    new_password: str = Field(
        min_length=6,
        max_length=100,
    )


# ============================================================
# TOKEN RESPONSE
# ============================================================

class TokenResponse(BaseModel):
    access_token: str

    refresh_token: str

    token_type: str = "bearer"


# ============================================================
# USER RESPONSE
# ============================================================

class UserResponse(BaseModel):
    id: int

    name: str

    email: EmailStr

    phone: str | None

    role: str

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )