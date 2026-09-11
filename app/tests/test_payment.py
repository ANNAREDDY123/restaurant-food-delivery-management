from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# GET PAYMENT - NOT FOUND
# ============================================================

def test_get_payment_not_found():
    response = client.get(
        "/payments/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"


# ============================================================
# UPDATE PAYMENT STATUS - NOT FOUND
# ============================================================

def test_update_payment_status_not_found():
    response = client.patch(
        "/payments/999999/status",
        json={
            "payment_status": "Success",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"


# ============================================================
# CREATE PAYMENT - ORDER NOT FOUND
# ============================================================

def test_create_payment_order_not_found():
    response = client.post(
        "/payments",
        json={
            "order_id": 999999,
            "payment_method": "UPI",
            "transaction_id": "TEST_TRANSACTION_001",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


# ============================================================
# CREATE PAYMENT - MISSING ORDER ID
# ============================================================

def test_create_payment_missing_order_id():
    response = client.post(
        "/payments",
        json={
            "payment_method": "UPI",
            "transaction_id": "TEST_TRANSACTION_002",
        },
    )

    assert response.status_code == 422


# ============================================================
# CREATE PAYMENT - MISSING PAYMENT METHOD
# ============================================================

def test_create_payment_missing_payment_method():
    response = client.post(
        "/payments",
        json={
            "order_id": 999999,
            "transaction_id": "TEST_TRANSACTION_003",
        },
    )

    assert response.status_code == 422


# ============================================================
# UPDATE PAYMENT STATUS - MISSING STATUS
# ============================================================

def test_update_payment_status_missing_status():
    response = client.patch(
        "/payments/999999/status",
        json={},
    )

    assert response.status_code == 422


# ============================================================
# UPDATE PAYMENT STATUS - INVALID BODY TYPE
# ============================================================

def test_update_payment_status_invalid_body():
    response = client.patch(
        "/payments/999999/status",
        json={
            "payment_status": 123,
        },
    )

    assert response.status_code == 422

# ============================================================
# CREATE PAYMENT - INVALID ORDER ID TYPE
# ============================================================

def test_create_payment_invalid_order_id_type():
    response = client.post(
        "/payments",
        json={
            "order_id": "invalid",
            "payment_method": "UPI",
            "transaction_id": "TEST_TRANSACTION_004",
        },
    )

    assert response.status_code == 422


# ============================================================
# GET PAYMENT - INVALID ORDER ID TYPE
# ============================================================

def test_get_payment_invalid_order_id_type():
    response = client.get(
        "/payments/invalid"
    )

    assert response.status_code == 422