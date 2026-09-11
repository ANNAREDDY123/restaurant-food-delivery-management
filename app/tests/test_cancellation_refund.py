from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# CANCEL ORDER - NOT FOUND
# ============================================================

def test_cancel_order_not_found():
    response = client.post(
        "/orders/999999/cancel",
        json={
            "reason": "Changed my mind",
            "cancelled_by": "Customer",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


# ============================================================
# PROCESS REFUND - ORDER NOT FOUND
# ============================================================

def test_process_refund_order_not_found():
    response = client.post(
        "/orders/999999/refund"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


# ============================================================
# GET REFUND - NOT FOUND
# ============================================================

def test_get_refund_not_found():
    response = client.get(
        "/orders/999999/refund"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Refund not found"


# ============================================================
# CANCEL ORDER - MISSING REASON
# ============================================================

def test_cancel_order_missing_reason():
    response = client.post(
        "/orders/999999/cancel",
        json={
            "cancelled_by": "Customer",
        },
    )

    assert response.status_code == 422