from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# GET ALL RESTAURANTS
# ============================================================

def test_get_all_restaurants():
    response = client.get("/restaurants")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# INVALID PAGE NUMBER
# ============================================================

def test_restaurants_invalid_page():
    response = client.get(
        "/restaurants",
        params={
            "page": 0,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Page must be greater than 0"
    )


# ============================================================
# INVALID LIMIT
# ============================================================

def test_restaurants_invalid_limit():
    response = client.get(
        "/restaurants",
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

def test_restaurants_limit_too_large():
    response = client.get(
        "/restaurants",
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

def test_restaurants_invalid_sort_field():
    response = client.get(
        "/restaurants",
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

def test_restaurants_invalid_sort_order():
    response = client.get(
        "/restaurants",
        params={
            "sort_order": "invalid",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "sort_order must be asc or desc"
    )


# ============================================================
# RESTAURANT NOT FOUND
# ============================================================

def test_get_restaurant_not_found():
    response = client.get(
        "/restaurants/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Restaurant not found"
    )


# ============================================================
# CREATE RESTAURANT WITHOUT TOKEN
# ============================================================

def test_create_restaurant_without_token():
    response = client.post(
        "/restaurants",
        json={
            "restaurant_name": "Test Restaurant",
            "address": "Test Address",
            "city": "Hyderabad",
            "phone": "9999999999",
            "cuisine_type": "Indian",
            "opening_time": "09:00:00",
            "closing_time": "22:00:00",
            "delivery_radius": 10,
        },
    )

    assert response.status_code == 401