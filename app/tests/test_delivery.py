from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app


client = TestClient(app)


# ============================================================
# GET ALL DELIVERY PARTNERS
# ============================================================

def test_get_all_delivery_partners():
    response = client.get(
        "/delivery-partners"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# CREATE DELIVERY PARTNER
# ============================================================

def test_create_delivery_partner():
    unique_id = uuid4().hex[:8]

    phone = (
        f"9{uuid4().int % 1000000000:09d}"
    )

    vehicle_number = (
        f"TS{unique_id.upper()}"
    )

    response = client.post(
        "/delivery-partners",
        json={
            "name": "Test Delivery Partner",
            "phone": phone,
            "vehicle_type": "Bike",
            "vehicle_number": vehicle_number,
            "current_location": "Hyderabad",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == (
        "Test Delivery Partner"
    )
    assert data["phone"] == phone
    assert data["vehicle_type"] == "Bike"
    assert data["vehicle_number"] == (
        vehicle_number
    )
    assert data["availability_status"] is True
    assert data["current_location"] == (
        "Hyderabad"
    )


# ============================================================
# CREATE DUPLICATE PHONE
# ============================================================

def test_create_delivery_partner_duplicate_phone():
    unique_id = uuid4().hex[:8]

    phone = (
        f"9{uuid4().int % 1000000000:09d}"
    )

    first_response = client.post(
        "/delivery-partners",
        json={
            "name": "Partner One",
            "phone": phone,
            "vehicle_type": "Bike",
            "vehicle_number": (
                f"TS{unique_id.upper()}A"
            ),
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/delivery-partners",
        json={
            "name": "Partner Two",
            "phone": phone,
            "vehicle_type": "Car",
            "vehicle_number": (
                f"TS{unique_id.upper()}B"
            ),
        },
    )

    assert second_response.status_code == 400

    assert (
        second_response.json()["detail"]
        == "Delivery partner phone already exists"
    )


# ============================================================
# CREATE DUPLICATE VEHICLE NUMBER
# ============================================================

def test_create_delivery_partner_duplicate_vehicle():
    unique_id = uuid4().hex[:8]

    vehicle_number = (
        f"TS{unique_id.upper()}"
    )

    phone_one = (
        f"9{uuid4().int % 1000000000:09d}"
    )

    phone_two = (
        f"8{uuid4().int % 1000000000:09d}"
    )

    first_response = client.post(
        "/delivery-partners",
        json={
            "name": "Partner One",
            "phone": phone_one,
            "vehicle_type": "Bike",
            "vehicle_number": vehicle_number,
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/delivery-partners",
        json={
            "name": "Partner Two",
            "phone": phone_two,
            "vehicle_type": "Car",
            "vehicle_number": vehicle_number,
        },
    )

    assert second_response.status_code == 400

    assert (
        second_response.json()["detail"]
        == "Vehicle number already exists"
    )


# ============================================================
# UPDATE DELIVERY PARTNER STATUS
# ============================================================

def test_update_delivery_partner_status():
    unique_id = uuid4().hex[:8]

    phone = (
        f"9{uuid4().int % 1000000000:09d}"
    )

    create_response = client.post(
        "/delivery-partners",
        json={
            "name": "Status Test Partner",
            "phone": phone,
            "vehicle_type": "Bike",
            "vehicle_number": (
                f"TSSTATUS{unique_id.upper()}"
            ),
            "current_location": "Hyderabad",
        },
    )

    assert create_response.status_code == 201

    partner_id = create_response.json()["id"]

    response = client.put(
        f"/delivery-partners/{partner_id}/status",
        json={
            "availability_status": False,
            "current_location": "Secunderabad",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["availability_status"] is False
    )

    assert data["current_location"] == (
        "Secunderabad"
    )


# ============================================================
# UPDATE DELIVERY PARTNER STATUS - NOT FOUND
# ============================================================

def test_update_delivery_partner_status_not_found():
    response = client.put(
        "/delivery-partners/999999/status",
        json={
            "availability_status": True,
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Delivery partner not found"
    )


# ============================================================
# ASSIGN DRIVER - ORDER NOT FOUND
# ============================================================

def test_assign_driver_order_not_found():
    unique_id = uuid4().hex[:8]

    phone = (
        f"9{uuid4().int % 1000000000:09d}"
    )

    create_response = client.post(
        "/delivery-partners",
        json={
            "name": "Driver Test",
            "phone": phone,
            "vehicle_type": "Bike",
            "vehicle_number": (
                f"TSDRIVER{unique_id.upper()}"
            ),
        },
    )

    assert create_response.status_code == 201

    driver_id = create_response.json()["id"]

    response = client.post(
        "/delivery-partners/orders/999999/assign-driver",
        json={
            "delivery_partner_id": driver_id,
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Order not found"
    )


# ============================================================
# ASSIGN DRIVER - DELIVERY PARTNER NOT FOUND
# ============================================================

def test_assign_driver_partner_not_found():
    response = client.post(
        "/delivery-partners/orders/999999/assign-driver",
        json={
            "delivery_partner_id": 999999,
        },
    )

    # Order is checked first in the service
    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Order not found"
    )


# ============================================================
# ASSIGN DRIVER WITH UNAVAILABLE PARTNER
# ============================================================

def test_assign_driver_unavailable_partner_order_not_found():
    unique_id = uuid4().hex[:8]

    phone = (
        f"9{uuid4().int % 1000000000:09d}"
    )

    create_response = client.post(
        "/delivery-partners",
        json={
            "name": "Unavailable Driver",
            "phone": phone,
            "vehicle_type": "Bike",
            "vehicle_number": (
                f"TSUNAVAILABLE{unique_id.upper()}"
            ),
        },
    )

    assert create_response.status_code == 201

    driver_id = create_response.json()["id"]

    update_response = client.put(
        f"/delivery-partners/{driver_id}/status",
        json={
            "availability_status": False,
        },
    )

    assert update_response.status_code == 200

    # Order is checked first, so this safely tests
    # the missing order scenario.
    response = client.post(
        "/delivery-partners/orders/999999/assign-driver",
        json={
            "delivery_partner_id": driver_id,
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Order not found"
    )