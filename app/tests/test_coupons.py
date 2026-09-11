from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from uuid import uuid4

from app.main import app


client = TestClient(app)


# ============================================================
# GET ALL COUPONS
# ============================================================

def test_get_all_coupons():
    response = client.get("/coupons")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# CREATE COUPON
# ============================================================

def test_create_coupon():
    unique_code = f"TEST{uuid4().hex[:8]}"

    start_date = datetime.utcnow()
    expiry_date = start_date + timedelta(days=30)

    response = client.post(
        "/coupons",
        json={
            "coupon_code": unique_code,
            "discount_type": "percentage",
            "discount_value": 10,
            "minimum_order_value": 100,
            "maximum_discount": 50,
            "start_date": start_date.isoformat(),
            "expiry_date": expiry_date.isoformat(),
            "usage_limit": 100,
            "status": True,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["coupon_code"] == unique_code.upper()
    assert data["discount_type"] == "percentage"
    assert data["discount_value"] == 10
    assert data["minimum_order_value"] == 100
    assert data["maximum_discount"] == 50
    assert data["usage_limit"] == 100
    assert data["status"] is True


# ============================================================
# CREATE DUPLICATE COUPON
# ============================================================

def test_create_duplicate_coupon():
    unique_code = f"DUP{uuid4().hex[:8]}"

    start_date = datetime.utcnow()
    expiry_date = start_date + timedelta(days=30)

    coupon_data = {
        "coupon_code": unique_code,
        "discount_type": "percentage",
        "discount_value": 10,
        "minimum_order_value": 100,
        "maximum_discount": 50,
        "start_date": start_date.isoformat(),
        "expiry_date": expiry_date.isoformat(),
        "usage_limit": 100,
        "status": True,
    }

    first_response = client.post(
        "/coupons",
        json=coupon_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/coupons",
        json=coupon_data,
    )

    assert second_response.status_code == 400

    assert (
        second_response.json()["detail"]
        == "Coupon code already exists"
    )


# ============================================================
# APPLY PERCENTAGE COUPON
# ============================================================

def test_apply_percentage_coupon():
    unique_code = f"PERCENT{uuid4().hex[:8]}"

    start_date = datetime.utcnow() - timedelta(days=1)
    expiry_date = datetime.utcnow() + timedelta(days=30)

    create_response = client.post(
        "/coupons",
        json={
            "coupon_code": unique_code,
            "discount_type": "percentage",
            "discount_value": 10,
            "minimum_order_value": 100,
            "maximum_discount": None,
            "start_date": start_date.isoformat(),
            "expiry_date": expiry_date.isoformat(),
            "usage_limit": 100,
            "status": True,
        },
    )

    assert create_response.status_code == 201

    response = client.post(
        "/coupons/apply",
        json={
            "coupon_code": unique_code,
            "customer_id": 1,
            "order_value": 1000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["coupon_code"] == unique_code.upper()
    assert data["order_value"] == 1000
    assert data["discount"] == 100
    assert data["final_amount"] == 900


# ============================================================
# APPLY COUPON WITH MAXIMUM DISCOUNT CAP
# ============================================================

def test_apply_coupon_maximum_discount():
    unique_code = f"MAX{uuid4().hex[:8]}"

    start_date = datetime.utcnow() - timedelta(days=1)
    expiry_date = datetime.utcnow() + timedelta(days=30)

    create_response = client.post(
        "/coupons",
        json={
            "coupon_code": unique_code,
            "discount_type": "percentage",
            "discount_value": 50,
            "minimum_order_value": 100,
            "maximum_discount": 200,
            "start_date": start_date.isoformat(),
            "expiry_date": expiry_date.isoformat(),
            "usage_limit": 100,
            "status": True,
        },
    )

    assert create_response.status_code == 201

    response = client.post(
        "/coupons/apply",
        json={
            "coupon_code": unique_code,
            "customer_id": 1,
            "order_value": 1000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["coupon_code"] == unique_code.upper()
    assert data["order_value"] == 1000
    assert data["discount"] == 200
    assert data["final_amount"] == 800


# ============================================================
# APPLY FIXED DISCOUNT COUPON
# ============================================================

def test_apply_fixed_discount_coupon():
    unique_code = f"FIXED{uuid4().hex[:8]}"

    start_date = datetime.utcnow() - timedelta(days=1)
    expiry_date = datetime.utcnow() + timedelta(days=30)

    create_response = client.post(
        "/coupons",
        json={
            "coupon_code": unique_code,
            "discount_type": "fixed",
            "discount_value": 150,
            "minimum_order_value": 100,
            "maximum_discount": None,
            "start_date": start_date.isoformat(),
            "expiry_date": expiry_date.isoformat(),
            "usage_limit": 100,
            "status": True,
        },
    )

    assert create_response.status_code == 201

    response = client.post(
        "/coupons/apply",
        json={
            "coupon_code": unique_code,
            "customer_id": 1,
            "order_value": 1000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["coupon_code"] == unique_code.upper()
    assert data["order_value"] == 1000
    assert data["discount"] == 150
    assert data["final_amount"] == 850


# ============================================================
# APPLY COUPON - NOT FOUND
# ============================================================

def test_apply_coupon_not_found():
    response = client.post(
        "/coupons/apply",
        json={
            "coupon_code": "INVALID_COUPON_999999",
            "customer_id": 1,
            "order_value": 1000,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Coupon not found"


# ============================================================
# APPLY INACTIVE COUPON
# ============================================================

def test_apply_inactive_coupon():
    unique_code = f"INACTIVE{uuid4().hex[:8]}"

    start_date = datetime.utcnow() - timedelta(days=1)
    expiry_date = datetime.utcnow() + timedelta(days=30)

    create_response = client.post(
        "/coupons",
        json={
            "coupon_code": unique_code,
            "discount_type": "percentage",
            "discount_value": 10,
            "minimum_order_value": 100,
            "maximum_discount": None,
            "start_date": start_date.isoformat(),
            "expiry_date": expiry_date.isoformat(),
            "usage_limit": 100,
            "status": False,
        },
    )

    assert create_response.status_code == 201

    response = client.post(
        "/coupons/apply",
        json={
            "coupon_code": unique_code,
            "customer_id": 1,
            "order_value": 1000,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Coupon is inactive"


# ============================================================
# APPLY EXPIRED COUPON
# ============================================================

def test_apply_expired_coupon():
    unique_code = f"EXPIRED{uuid4().hex[:8]}"

    start_date = datetime.utcnow() - timedelta(days=30)
    expiry_date = datetime.utcnow() - timedelta(days=1)

    create_response = client.post(
        "/coupons",
        json={
            "coupon_code": unique_code,
            "discount_type": "percentage",
            "discount_value": 10,
            "minimum_order_value": 100,
            "maximum_discount": None,
            "start_date": start_date.isoformat(),
            "expiry_date": expiry_date.isoformat(),
            "usage_limit": 100,
            "status": True,
        },
    )

    assert create_response.status_code == 201

    response = client.post(
        "/coupons/apply",
        json={
            "coupon_code": unique_code,
            "customer_id": 1,
            "order_value": 1000,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Coupon has expired"


# ============================================================
# APPLY COUPON - MINIMUM ORDER VALUE NOT SATISFIED
# ============================================================

def test_apply_coupon_minimum_order_value():
    unique_code = f"MINORDER{uuid4().hex[:8]}"

    start_date = datetime.utcnow() - timedelta(days=1)
    expiry_date = datetime.utcnow() + timedelta(days=30)

    create_response = client.post(
        "/coupons",
        json={
            "coupon_code": unique_code,
            "discount_type": "percentage",
            "discount_value": 10,
            "minimum_order_value": 1000,
            "maximum_discount": None,
            "start_date": start_date.isoformat(),
            "expiry_date": expiry_date.isoformat(),
            "usage_limit": 100,
            "status": True,
        },
    )

    assert create_response.status_code == 201

    response = client.post(
        "/coupons/apply",
        json={
            "coupon_code": unique_code,
            "customer_id": 1,
            "order_value": 500,
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Minimum order value not satisfied"
    )


# ============================================================
# APPLY COUPON - USAGE LIMIT EXCEEDED
# ============================================================

def test_apply_coupon_usage_limit_exceeded():
    unique_code = f"LIMIT{uuid4().hex[:8]}"

    start_date = datetime.utcnow() - timedelta(days=1)
    expiry_date = datetime.utcnow() + timedelta(days=30)

    # Create coupon with usage limit of 1
    create_response = client.post(
        "/coupons",
        json={
            "coupon_code": unique_code,
            "discount_type": "percentage",
            "discount_value": 10,
            "minimum_order_value": 100,
            "maximum_discount": None,
            "start_date": start_date.isoformat(),
            "expiry_date": expiry_date.isoformat(),
            "usage_limit": 1,
            "status": True,
        },
    )

    assert create_response.status_code == 201

    # First use should succeed
    first_response = client.post(
        "/coupons/apply",
        json={
            "coupon_code": unique_code,
            "customer_id": 1,
            "order_value": 1000,
        },
    )

    assert first_response.status_code == 200

    # Second use should fail
    second_response = client.post(
        "/coupons/apply",
        json={
            "coupon_code": unique_code,
            "customer_id": 1,
            "order_value": 1000,
        },
    )

    assert second_response.status_code == 400

    assert (
        second_response.json()["detail"]
        == "Coupon usage limit exceeded"
    )