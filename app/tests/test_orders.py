from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# GET ALL ORDERS
# ============================================================

def test_get_all_orders():
    response = client.get("/orders")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# GET ORDER NOT FOUND
# ============================================================

def test_get_order_not_found():
    response = client.get("/orders/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


# ============================================================
# CANCEL ORDER NOT FOUND
# ============================================================

def test_cancel_order_not_found():
    response = client.post(
        "/orders/999999/cancel",
        json={
            "reason": "Customer request",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


# ============================================================
# UPDATE ORDER STATUS NOT FOUND
# ============================================================

def test_update_order_status_not_found():
    response = client.put(
        "/orders/999999/status",
        json={
            "order_status": "Accepted"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


# ============================================================
# INVALID PAGE NUMBER
# ============================================================

def test_orders_invalid_page():
    response = client.get(
        "/orders",
        params={
            "page": 0,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Page must be greater than 0"
    )


# ============================================================
# NEGATIVE PAGE NUMBER
# ============================================================

def test_orders_negative_page():
    response = client.get(
        "/orders",
        params={
            "page": -1,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Page must be greater than 0"
    )


# ============================================================
# INVALID LIMIT
# ============================================================

def test_orders_invalid_limit():
    response = client.get(
        "/orders",
        params={
            "limit": 0,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Limit must be between 1 and 100"
    )


# ============================================================
# LIMIT GREATER THAN 100
# ============================================================

def test_orders_limit_too_large():
    response = client.get(
        "/orders",
        params={
            "limit": 101,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Limit must be between 1 and 100"
    )


# ============================================================
# INVALID SORT FIELD
# ============================================================

def test_orders_invalid_sort_field():
    response = client.get(
        "/orders",
        params={
            "sort_by": "invalid_field",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Invalid sort_by field"
    )


# ============================================================
# INVALID SORT ORDER
# ============================================================

def test_orders_invalid_sort_order():
    response = client.get(
        "/orders",
        params={
            "sort_order": "wrong",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "sort_order must be asc or desc"
    )


# ============================================================
# INVALID DATE RANGE
# ============================================================

def test_orders_invalid_date_range():
    response = client.get(
        "/orders",
        params={
            "start_date": "2026-12-31T00:00:00",
            "end_date": "2026-01-01T00:00:00",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Start date cannot be greater than end date"
    )


# ============================================================
# VALID PAGINATION
# ============================================================

def test_orders_valid_pagination():
    response = client.get(
        "/orders",
        params={
            "page": 1,
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 5


# ============================================================
# PAGE BEYOND AVAILABLE DATA
# ============================================================

def test_orders_page_beyond_available_data():
    response = client.get(
        "/orders",
        params={
            "page": 999999,
            "limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data == []


# ============================================================
# DEFAULT PAGINATION
# ============================================================

def test_orders_default_pagination():
    response = client.get("/orders")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 10


# ============================================================
# FILTER BY ORDER STATUS
# ============================================================

def test_orders_filter_by_status():
    response = client.get(
        "/orders",
        params={
            "order_status": "Pending",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for order in data:
        assert order["order_status"] == "Pending"


# ============================================================
# FILTER BY PAYMENT STATUS
# ============================================================

def test_orders_filter_by_payment_status():
    response = client.get(
        "/orders",
        params={
            "payment_status": "Pending",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for order in data:
        assert order["payment_status"] == "Pending"


# ============================================================
# VALID SORT ASCENDING
# ============================================================

def test_orders_sort_ascending():
    response = client.get(
        "/orders",
        params={
            "sort_by": "id",
            "sort_order": "asc",
        },
    )

    assert response.status_code == 200


# ============================================================
# VALID SORT DESCENDING
# ============================================================

def test_orders_sort_descending():
    response = client.get(
        "/orders",
        params={
            "sort_by": "id",
            "sort_order": "desc",
        },
    )

    assert response.status_code == 200


# ============================================================
# CREATE ORDER - CART NOT FOUND
# ============================================================

def test_create_order_cart_not_found():
    response = client.post(
        "/orders",
        json={
            "customer_id": 999999,
            "address_id": 999999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Cart not found"