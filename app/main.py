from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# Import all models before creating tables
import app.models

from app.routes.auth import router as auth_router
from app.routes.restaurant import router as restaurant_router
from app.routes.customers import router as customers_router
from app.routes.addresses import router as addresses_router

from app.routes import cart
from app.routes import menu
from app.routes import coupons
from app.routes import orders
from app.routes import delivery
from app.routes import tracking
from app.routes import payment
from app.routes import cancellation_refund
from app.routes import reviews
from app.routes import dashboard
from app.routes import admin_analytics

from app.utils.exception_handlers import (
    register_exception_handlers,
)


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Restaurant & Food Delivery Management System",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=[
        "*",
    ],
    allow_headers=[
        "*",
    ],
)


# ============================================================
# EXCEPTION HANDLERS
# ============================================================

register_exception_handlers(app)


# ============================================================
# REGISTER ROUTES
# ============================================================

app.include_router(auth_router)
app.include_router(restaurant_router)
app.include_router(menu.router)
app.include_router(customers_router)
app.include_router(addresses_router)
app.include_router(cart.router)
app.include_router(coupons.router)
app.include_router(orders.router)
app.include_router(delivery.router)
app.include_router(tracking.router)
app.include_router(payment.router)
app.include_router(cancellation_refund.router)
app.include_router(reviews.router)
app.include_router(dashboard.router)
app.include_router(admin_analytics.router)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": (
            "Restaurant & Food Delivery API is running"
        )
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }