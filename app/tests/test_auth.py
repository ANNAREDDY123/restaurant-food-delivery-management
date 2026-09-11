from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app


client = TestClient(app)


# ============================================================
# REGISTER USER
# ============================================================

def test_register_user():
    unique_id = uuid4().hex[:8]

    email = f"testuser_{unique_id}@example.com"
    phone = f"9{uuid4().int % 1000000000:09d}"

    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "phone": phone,
            "password": "Test123",
            "role": "Customer",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["name"] == "Test User"
    assert data["role"] == "Customer"


# ============================================================
# INVALID LOGIN
# ============================================================

def test_invalid_login():
    response = client.post(
        "/auth/login",
        json={
            "email": "wronguser@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401


# ============================================================
# REGISTER WITH DUPLICATE EMAIL
# ============================================================

def test_register_duplicate_email():
    unique_id = uuid4().hex[:8]

    email = f"duplicate_{unique_id}@example.com"

    phone1 = (
        f"9{uuid4().int % 1000000000:09d}"
    )

    phone2 = (
        f"8{uuid4().int % 1000000000:09d}"
    )

    first_response = client.post(
        "/auth/register",
        json={
            "name": "First User",
            "email": email,
            "phone": phone1,
            "password": "Test123",
            "role": "Customer",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json={
            "name": "Second User",
            "email": email,
            "phone": phone2,
            "password": "Test123",
            "role": "Customer",
        },
    )

    assert second_response.status_code == 400

    assert (
        second_response.json()["detail"]
        == "Email already registered"
    )


# ============================================================
# REGISTER WITH INVALID EMAIL
# ============================================================

def test_register_invalid_email():
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "invalid-email",
            "phone": "9876543210",
            "password": "Test123",
            "role": "Customer",
        },
    )

    assert response.status_code == 422


# ============================================================
# REGISTER WITH SHORT PASSWORD
# ============================================================

def test_register_short_password():
    unique_id = uuid4().hex[:8]

    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": (
                f"shortpassword_{unique_id}"
                "@example.com"
            ),
            "phone": (
                f"9{uuid4().int % 1000000000:09d}"
            ),
            "password": "123",
            "role": "Customer",
        },
    )

    assert response.status_code == 422


# ============================================================
# LOGIN WITH MISSING USER
# ============================================================

def test_login_user_not_found():
    response = client.post(
        "/auth/login",
        json={
            "email": (
                f"missing_{uuid4().hex[:8]}"
                "@example.com"
            ),
            "password": "Test123",
        },
    )

    assert response.status_code == 401

    assert (
        response.json()["detail"]
        == "Invalid email or password"
    )