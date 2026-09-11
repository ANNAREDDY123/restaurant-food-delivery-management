from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# GET CART - CART NOT FOUND
# ============================================================

def test_get_cart_not_found():
    response = client.get(
        "/cart",
        params={
            "customer_id": 999999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Cart not found"


# ============================================================
# ADD CART ITEM - CUSTOMER NOT FOUND
# ============================================================

def test_add_cart_item_customer_not_found():
    response = client.post(
        "/cart/items",
        json={
            "customer_id": 999999,
            "food_item_id": 1,
            "quantity": 2,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


# ============================================================
# ADD CART ITEM - FOOD ITEM NOT FOUND
# ============================================================

def test_add_cart_item_food_item_not_found():
    response = client.post(
        "/cart/items",
        json={
            "customer_id": 1,
            "food_item_id": 999999,
            "quantity": 2,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Food item not found"


# ============================================================
# UPDATE CART ITEM - CART NOT FOUND
# ============================================================

def test_update_cart_item_cart_not_found():
    response = client.put(
        "/cart/items/999999",
        params={
            "customer_id": 999999,
        },
        json={
            "quantity": 2,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Cart not found"


# ============================================================
# UPDATE CART ITEM - ITEM NOT FOUND
# ============================================================

def test_update_cart_item_not_found():
    response = client.put(
        "/cart/items/999999",
        params={
            "customer_id": 1,
        },
        json={
            "quantity": 2,
        },
    )

    assert response.status_code in [404]


# ============================================================
# REMOVE CART ITEM - CART NOT FOUND
# ============================================================

def test_remove_cart_item_cart_not_found():
    response = client.delete(
        "/cart/items/999999",
        params={
            "customer_id": 999999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Cart not found"


# ============================================================
# REMOVE CART ITEM - ITEM NOT FOUND
# ============================================================

def test_remove_cart_item_not_found():
    response = client.delete(
        "/cart/items/999999",
        params={
            "customer_id": 1,
        },
    )

    assert response.status_code in [404]


# ============================================================
# CLEAR CART - CART NOT FOUND
# ============================================================

def test_clear_cart_not_found():
    response = client.delete(
        "/cart/clear",
        params={
            "customer_id": 999999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Cart not found"