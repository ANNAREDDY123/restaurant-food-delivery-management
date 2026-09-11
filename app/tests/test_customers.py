from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app


client = TestClient(app)


# ============================================================
# GET ALL CUSTOMERS
# ============================================================

def test_get_all_customers():
    response = client.get("/customers")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# INVALID PAGE NUMBER
# ============================================================

def test_customers_invalid_page():
    response = client.get(
        "/customers",
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

def test_customers_invalid_limit():
    response = client.get(
        "/customers",
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

def test_customers_limit_too_large():
    response = client.get(
        "/customers",
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

def test_customers_invalid_sort_field():
    response = client.get(
        "/customers",
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

def test_customers_invalid_sort_order():
    response = client.get(
        "/customers",
        params={
            "sort_order": "invalid",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "sort_order must be asc or desc"
    )


# ============================================================
# GET CUSTOMER NOT FOUND
# ============================================================

def test_get_customer_not_found():
    response = client.get(
        "/customers/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Customer not found"
    )


# ============================================================
# UPDATE CUSTOMER NOT FOUND
# ============================================================

def test_update_customer_not_found():
    response = client.put(
        "/customers/999999",
        json={
            "name": "Updated Customer",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Customer not found"
    )


# ============================================================
# GET CUSTOMER ADDRESSES NOT FOUND
# ============================================================

def test_get_customer_addresses_not_found():
    response = client.get(
        "/customers/999999/addresses"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Customer not found"
    )


# ============================================================
# CREATE CUSTOMER ADDRESS NOT FOUND
# ============================================================

def test_create_customer_address_not_found():
    response = client.post(
        "/customers/999999/addresses",
        json={
            "address_line": "Test Address",
            "city": "Hyderabad",
            "pincode": "500001",
            "latitude": 17.3850,
            "longitude": 78.4867,
            "address_type": "Home",
            "is_default": True,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Customer not found"
    )


# ============================================================
# CREATE CUSTOMER
# ============================================================

def test_create_customer():
    unique_id = uuid4().hex[:8]

    email = (
        f"customer_{unique_id}@example.com"
    )

    phone = (
        f"8{uuid4().int % 1000000000:09d}"
    )

    response = client.post(
        "/customers",
        json={
            "name": "Test Customer",
            "email": email,
            "phone": phone,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Customer"
    assert data["email"] == email
    assert data["phone"] == phone


# ============================================================
# CREATE DUPLICATE CUSTOMER EMAIL
# ============================================================

def test_create_duplicate_customer_email():
    unique_id = uuid4().hex[:8]

    email = (
        f"duplicate_{unique_id}@example.com"
    )

    phone1 = (
        f"7{uuid4().int % 1000000000:09d}"
    )

    phone2 = (
        f"6{uuid4().int % 1000000000:09d}"
    )

    first_response = client.post(
        "/customers",
        json={
            "name": "Customer One",
            "email": email,
            "phone": phone1,
        },
    )

    assert first_response.status_code == 201

    response = client.post(
        "/customers",
        json={
            "name": "Customer Two",
            "email": email,
            "phone": phone2,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Customer with this email already exists"
    )


# ============================================================
# CREATE DUPLICATE CUSTOMER PHONE
# ============================================================

def test_create_duplicate_customer_phone():
    unique_id = uuid4().hex[:8]

    email1 = (
        f"customer1_{unique_id}@example.com"
    )

    email2 = (
        f"customer2_{unique_id}@example.com"
    )

    phone = (
        f"9{uuid4().int % 1000000000:09d}"
    )

    first_response = client.post(
        "/customers",
        json={
            "name": "Customer One",
            "email": email1,
            "phone": phone,
        },
    )

    assert first_response.status_code == 201

    response = client.post(
        "/customers",
        json={
            "name": "Customer Two",
            "email": email2,
            "phone": phone,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Customer with this phone already exists"
    )