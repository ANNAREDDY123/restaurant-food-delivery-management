from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# ADMIN ANALYTICS - SUCCESS
# ============================================================

def test_admin_analytics_success():
    response = client.get(
        "/admin/analytics"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)


# ============================================================
# ADMIN ANALYTICS - BASIC TOTALS
# ============================================================

def test_admin_analytics_basic_totals():
    response = client.get(
        "/admin/analytics"
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_restaurants" in data
    assert "total_customers" in data
    assert "total_orders" in data
    assert "total_revenue" in data
    assert "total_refunds" in data
    assert "active_delivery_partners" in data


# ============================================================
# ADMIN ANALYTICS - ANALYTICS DATA
# ============================================================

def test_admin_analytics_response_structure():
    response = client.get(
        "/admin/analytics"
    )

    assert response.status_code == 200

    data = response.json()

    assert "top_restaurants" in data
    assert "top_food_items" in data
    assert "most_popular_cuisine" in data
    assert "daily_orders" in data
    assert "monthly_revenue" in data
    assert "cancellation_rate" in data


# ============================================================
# ADMIN ANALYTICS - DATA TYPES
# ============================================================

def test_admin_analytics_data_types():
    response = client.get(
        "/admin/analytics"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data["total_restaurants"],
        int,
    )

    assert isinstance(
        data["total_customers"],
        int,
    )

    assert isinstance(
        data["total_orders"],
        int,
    )

    assert isinstance(
        data["top_restaurants"],
        list,
    )

    assert isinstance(
        data["top_food_items"],
        list,
    )

    assert isinstance(
        data["daily_orders"],
        list,
    )

    assert isinstance(
        data["monthly_revenue"],
        list,
    )