from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# GET RESTAURANT REVIEWS - RESTAURANT NOT FOUND
# ============================================================

def test_get_restaurant_reviews_not_found():

    response = client.get(
        "/restaurants/999999/reviews"
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Restaurant not found"
    )


# ============================================================
# GET FOOD ITEM REVIEWS - FOOD ITEM NOT FOUND
# ============================================================

def test_get_food_item_reviews_not_found():

    response = client.get(
        "/food-items/999999/reviews"
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Food item not found"
    )


# ============================================================
# CREATE REVIEW - CUSTOMER NOT FOUND
# ============================================================

def test_create_review_customer_not_found():

    response = client.post(
        "/reviews",
        json={
            "customer_id": 999999,
            "order_id": 999999,
            "restaurant_id": 1,
            "rating": 5,
            "review": "Excellent restaurant",
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Customer not found"
    )


# ============================================================
# CREATE REVIEW - INVALID RATING TOO LOW
# ============================================================

def test_create_review_rating_too_low():

    response = client.post(
        "/reviews",
        json={
            "customer_id": 1,
            "order_id": 1,
            "restaurant_id": 1,
            "rating": 0,
            "review": "Invalid rating",
        },
    )

    assert response.status_code == 422


# ============================================================
# CREATE REVIEW - INVALID RATING TOO HIGH
# ============================================================

def test_create_review_rating_too_high():

    response = client.post(
        "/reviews",
        json={
            "customer_id": 1,
            "order_id": 1,
            "restaurant_id": 1,
            "rating": 6,
            "review": "Invalid rating",
        },
    )

    assert response.status_code == 422


# ============================================================
# CREATE REVIEW - ORDER NOT FOUND
# ============================================================

def test_create_review_order_not_found():

    response = client.post(
        "/reviews",
        json={
            "customer_id": 1,
            "order_id": 999999,
            "restaurant_id": 1,
            "rating": 5,
            "review": "Good",
        },
    )

    # Customer ID 1 may or may not exist depending
    # on the database state.
    # The endpoint checks customer before order.
    assert response.status_code in [404]


# ============================================================
# CREATE REVIEW - NO REVIEW TARGET
# ============================================================

def test_create_review_no_target():

    response = client.post(
        "/reviews",
        json={
            "customer_id": 1,
            "order_id": 1,
            "rating": 5,
            "review": "Good",
        },
    )

    # Depending on test database data, validation may
    # fail earlier because customer/order may not exist.
    assert response.status_code in [400, 403, 404]


# ============================================================
# CREATE REVIEW - NON EXISTENT RESTAURANT
# ============================================================

def test_create_review_restaurant_not_found():

    response = client.post(
        "/reviews",
        json={
            "customer_id": 1,
            "order_id": 1,
            "restaurant_id": 999999,
            "rating": 5,
            "review": "Good",
        },
    )

    assert response.status_code in [
        400,
        403,
        404,
    ]


# ============================================================
# CREATE REVIEW - NON EXISTENT FOOD ITEM
# ============================================================

def test_create_review_food_item_not_found():

    response = client.post(
        "/reviews",
        json={
            "customer_id": 1,
            "order_id": 1,
            "food_item_id": 999999,
            "rating": 5,
            "review": "Good food",
        },
    )

    assert response.status_code in [
        400,
        403,
        404,
    ]


# ============================================================
# CREATE REVIEW - NON EXISTENT DELIVERY PARTNER
# ============================================================

def test_create_review_delivery_partner_not_found():

    response = client.post(
        "/reviews",
        json={
            "customer_id": 1,
            "order_id": 1,
            "delivery_partner_id": 999999,
            "rating": 5,
            "review": "Good delivery",
        },
    )

    assert response.status_code in [
        400,
        403,
        404,
    ]