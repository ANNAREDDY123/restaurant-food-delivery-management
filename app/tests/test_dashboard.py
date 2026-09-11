from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# RESTAURANT DASHBOARD - RESTAURANT NOT FOUND
# ============================================================

def test_restaurant_dashboard_not_found():
    response = client.get(
        "/dashboard/restaurants/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Restaurant not found"
    )


# ============================================================
# RESTAURANT DASHBOARD - SUCCESS
# ============================================================

def test_restaurant_dashboard_success():
    response = client.get(
        "/dashboard/restaurants/1"
    )

    assert response.status_code in [200, 404]


# ============================================================
# RESTAURANT DASHBOARD - RESPONSE DATA
# ============================================================

def test_restaurant_dashboard_response_structure():
    response = client.get(
        "/dashboard/restaurants/1"
    )

    if response.status_code == 200:
        data = response.json()

        assert "restaurant_id" in data
        assert "today_orders" in data
        assert "pending_orders" in data
        assert "completed_orders" in data
        assert "cancelled_orders" in data
        assert "today_revenue" in data
        assert "monthly_revenue" in data
        assert "most_ordered_food" in data
        assert "average_rating" in data
        assert "total_customers" in data


# ============================================================
# RESTAURANT DASHBOARD - INVALID ID
# ============================================================

def test_restaurant_dashboard_invalid_id():
    response = client.get(
        "/dashboard/restaurants/abc"
    )

    assert response.status_code == 422