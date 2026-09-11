from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# GET TRACKING - ORDER NOT FOUND
# ============================================================

def test_get_tracking_order_not_found():
    response = client.get(
        "/orders/999999/tracking"
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Order not found"
    )


# ============================================================
# CREATE TRACKING - ORDER NOT FOUND
# ============================================================

def test_create_tracking_order_not_found():
    response = client.post(
        "/orders/999999/tracking",
        json={
            "status": "Accepted",
            "location": "Hyderabad",
            "remarks": "Order accepted",
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Order not found"
    )


# ============================================================
# CREATE TRACKING WITH MINIMAL DATA - ORDER NOT FOUND
# ============================================================

def test_create_tracking_minimal_data_order_not_found():
    response = client.post(
        "/orders/999998/tracking",
        json={
            "status": "Preparing",
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Order not found"
    )


# ============================================================
# TRACKING VALIDATION - MISSING STATUS
# ============================================================

def test_create_tracking_missing_status():
    response = client.post(
        "/orders/999997/tracking",
        json={
            "location": "Hyderabad",
            "remarks": "Testing",
        },
    )

    assert response.status_code == 422


# ============================================================
# TRACKING VALIDATION - EMPTY REQUEST
# ============================================================

def test_create_tracking_empty_request():
    response = client.post(
        "/orders/999996/tracking",
        json={}
    )

    assert response.status_code == 422