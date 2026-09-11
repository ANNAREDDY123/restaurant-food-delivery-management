from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# GET ALL FOOD ITEMS
# ============================================================

def test_get_all_food_items():
    response = client.get("/menu/items")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# GET FOOD ITEM NOT FOUND
# ============================================================

def test_get_food_item_not_found():
    response = client.get("/menu/items/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Food item not found"


# ============================================================
# CREATE FOOD ITEM WITH INVALID RESTAURANT
# ============================================================

def test_create_food_item_invalid_restaurant():
    response = client.post(
        "/menu/items",
        json={
            "restaurant_id": 999999,
            "category": "Pizza",
            "name": "Test Pizza",
            "description": "Test food item",
            "price": 250,
            "preparation_time": 20,
            "availability": True,
            "vegetarian": True,
            "spicy_level": 2,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Restaurant not found"


# ============================================================
# UPDATE FOOD ITEM NOT FOUND
# ============================================================

def test_update_food_item_not_found():
    response = client.put(
        "/menu/items/999999",
        json={
            "name": "Updated Food Item",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Food item not found"


# ============================================================
# DELETE FOOD ITEM NOT FOUND
# ============================================================

def test_delete_food_item_not_found():
    response = client.delete(
        "/menu/items/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Food item not found"

# ============================================================
# INVALID PRICE RANGE
# ============================================================

def test_invalid_price_range():
    response = client.get(
        "/menu/items",
        params={
            "min_price": 500,
            "max_price": 100,
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Minimum price cannot be greater than maximum price"
    )


# ============================================================
# NEGATIVE MINIMUM PRICE
# ============================================================

def test_negative_minimum_price():
    response = client.get(
        "/menu/items",
        params={
            "min_price": -10,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Minimum price cannot be negative"
    )


# ============================================================
# INVALID SORT FIELD
# ============================================================

def test_invalid_sort_field():
    response = client.get(
        "/menu/items",
        params={
            "sort_by": "invalid_field",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Invalid sort_by field"
    )


# ============================================================
# INVALID SORT ORDER
# ============================================================

def test_invalid_sort_order():
    response = client.get(
        "/menu/items",
        params={
            "sort_order": "wrong",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "sort_order must be asc or desc"
    )

# ============================================================
# INVALID PAGE NUMBER
# ============================================================

def test_invalid_page_number():
    response = client.get(
        "/menu/items",
        params={
            "page": 0,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Page must be greater than 0"
    )


# ============================================================
# INVALID LIMIT - TOO SMALL
# ============================================================

def test_invalid_limit_too_small():
    response = client.get(
        "/menu/items",
        params={
            "limit": 0,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Limit must be between 1 and 100"
    )


# ============================================================
# INVALID LIMIT - TOO LARGE
# ============================================================

def test_invalid_limit_too_large():
    response = client.get(
        "/menu/items",
        params={
            "limit": 101,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Limit must be between 1 and 100"
    )


# ============================================================
# VALID PAGINATION
# ============================================================

def test_valid_pagination():
    response = client.get(
        "/menu/items",
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
# PAGINATION BOUNDARY - PAGE 1 WITH LIMIT 1
# ============================================================

def test_pagination_limit_one():
    response = client.get(
        "/menu/items",
        params={
            "page": 1,
            "limit": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 1


# ============================================================
# PAGINATION BOUNDARY - MAXIMUM LIMIT
# ============================================================

def test_pagination_maximum_limit():
    response = client.get(
        "/menu/items",
        params={
            "page": 1,
            "limit": 100,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 100


# ============================================================
# PAGINATION - PAGE BEYOND AVAILABLE DATA
# ============================================================

def test_pagination_page_beyond_available_data():
    response = client.get(
        "/menu/items",
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
# PAGINATION - DIFFERENT PAGE AND LIMIT COMBINATIONS
# ============================================================

def test_pagination_page_two_limit_one():
    response = client.get(
        "/menu/items",
        params={
            "page": 2,
            "limit": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 1


def test_pagination_page_two_limit_five():
    response = client.get(
        "/menu/items",
        params={
            "page": 2,
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 5


def test_pagination_page_ten_limit_ten():
    response = client.get(
        "/menu/items",
        params={
            "page": 10,
            "limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 10


# ============================================================
# PAGINATION - MAXIMUM PAGE WITH MINIMUM LIMIT
# ============================================================

def test_pagination_large_page_small_limit():
    response = client.get(
        "/menu/items",
        params={
            "page": 1000,
            "limit": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 1

# ============================================================
# PAGINATION - PAGE WITH MAXIMUM LIMIT
# ============================================================

def test_pagination_page_two_maximum_limit():
    response = client.get(
        "/menu/items",
        params={
            "page": 2,
            "limit": 100,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 100


# ============================================================
# PAGINATION - NEGATIVE PAGE NUMBER
# ============================================================

def test_negative_page_number():
    response = client.get(
        "/menu/items",
        params={
            "page": -1,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Page must be greater than 0"
    )


# ============================================================
# PAGINATION - NEGATIVE LIMIT
# ============================================================

def test_negative_limit():
    response = client.get(
        "/menu/items",
        params={
            "limit": -5,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Limit must be between 1 and 100"
    )

# ============================================================
# PAGINATION DEFAULTS
# ============================================================

def test_pagination_default_values():
    response = client.get(
        "/menu/items"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    # Default limit is 10
    assert len(data) <= 10


# ============================================================
# DEFAULT PAGE WITH CUSTOM LIMIT
# ============================================================

def test_default_page_with_custom_limit():
    response = client.get(
        "/menu/items",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 5


# ============================================================
# CUSTOM PAGE WITH DEFAULT LIMIT
# ============================================================

def test_custom_page_with_default_limit():
    response = client.get(
        "/menu/items",
        params={
            "page": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    # Default limit is 10
    assert len(data) <= 10

# ============================================================
# CREATE FOOD ITEM - INVALID PRICE
# ============================================================

def test_create_food_item_invalid_price():
    response = client.post(
        "/menu/items",
        json={
            "restaurant_id": 1,
            "category": "Pizza",
            "name": "Invalid Price Pizza",
            "description": "Test item",
            "price": -100,
            "preparation_time": 20,
            "availability": True,
            "vegetarian": True,
            "spicy_level": 2,
        },
    )

    assert response.status_code == 422


# ============================================================
# CREATE FOOD ITEM - INVALID SPICY LEVEL
# ============================================================

def test_create_food_item_invalid_spicy_level():
    response = client.post(
        "/menu/items",
        json={
            "restaurant_id": 1,
            "category": "Pizza",
            "name": "Very Spicy Pizza",
            "description": "Test item",
            "price": 250,
            "preparation_time": 20,
            "availability": True,
            "vegetarian": False,
            "spicy_level": 10,
        },
    )

    assert response.status_code == 422


# ============================================================
# CREATE FOOD ITEM - INVALID PREPARATION TIME
# ============================================================

def test_create_food_item_invalid_preparation_time():
    response = client.post(
        "/menu/items",
        json={
            "restaurant_id": 1,
            "category": "Pizza",
            "name": "Quick Pizza",
            "description": "Test item",
            "price": 250,
            "preparation_time": 0,
            "availability": True,
            "vegetarian": True,
            "spicy_level": 2,
        },
    )

    assert response.status_code == 422


# ============================================================
# CREATE FOOD ITEM - EMPTY NAME
# ============================================================

def test_create_food_item_invalid_name():
    response = client.post(
        "/menu/items",
        json={
            "restaurant_id": 1,
            "category": "Pizza",
            "name": "",
            "description": "Test item",
            "price": 250,
            "preparation_time": 20,
            "availability": True,
            "vegetarian": True,
            "spicy_level": 2,
        },
    )

    assert response.status_code == 422