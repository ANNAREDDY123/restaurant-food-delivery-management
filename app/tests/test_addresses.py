from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app


client = TestClient(app)


# ============================================================
# UPDATE ADDRESS - NOT FOUND
# ============================================================

def test_update_address_not_found():
    response = client.put(
        "/addresses/999999",
        json={
            "city": "Hyderabad",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"


# ============================================================
# UPDATE ADDRESS - EMPTY REQUEST
# ============================================================

def test_update_address_empty_data_not_found():
    response = client.put(
        "/addresses/999999",
        json={},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"


# ============================================================
# UPDATE REAL ADDRESS
# ============================================================

def test_update_real_address():
    unique_id = uuid4().hex[:8]

    # Create customer
    customer_response = client.post(
        "/customers",
        json={
            "name": "Address Test User",
            "email": f"address_{unique_id}@example.com",
            "phone": f"9{uuid4().int % 1000000000:09d}",
        },
    )

    assert customer_response.status_code == 201

    customer = customer_response.json()
    customer_id = customer["id"]

    # Create address
    address_response = client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "address_line": "123 Test Street",
            "city": "Hyderabad",
            "pincode": "500001",
            "address_type": "Home",
            "is_default": False,
        },
    )

    assert address_response.status_code == 201

    address = address_response.json()
    address_id = address["id"]

    # Update address
    response = client.put(
        f"/addresses/{address_id}",
        json={
            "city": "Bengaluru",
            "pincode": "560001",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == address_id
    assert data["customer_id"] == customer_id
    assert data["city"] == "Bengaluru"
    assert data["pincode"] == "560001"
    assert data["address_line"] == "123 Test Street"


# ============================================================
# DEFAULT ADDRESS SWITCHING
# ============================================================

def test_switch_default_address():
    unique_id = uuid4().hex[:8]

    # Create customer
    customer_response = client.post(
        "/customers",
        json={
            "name": "Default Address User",
            "email": f"default_{unique_id}@example.com",
            "phone": f"8{uuid4().int % 1000000000:09d}",
        },
    )

    assert customer_response.status_code == 201

    customer_id = customer_response.json()["id"]

    # Create first address
    first_address_response = client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "address_line": "First Address Street",
            "city": "Hyderabad",
            "pincode": "500001",
            "address_type": "Home",
            "is_default": True,
        },
    )

    assert first_address_response.status_code == 201

    first_address = first_address_response.json()

    # Create second address
    second_address_response = client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "address_line": "Second Address Street",
            "city": "Bengaluru",
            "pincode": "560001",
            "address_type": "Work",
            "is_default": False,
        },
    )

    assert second_address_response.status_code == 201

    second_address = second_address_response.json()

    # Make second address the default
    update_response = client.put(
        f"/addresses/{second_address['id']}",
        json={
            "is_default": True,
        },
    )

    assert update_response.status_code == 200

    assert (
        update_response.json()["is_default"]
        is True
    )

    # Get all addresses and verify switching
    addresses_response = client.get(
        f"/customers/{customer_id}/addresses"
    )

    assert addresses_response.status_code == 200

    addresses = addresses_response.json()

    first_address_data = next(
        address
        for address in addresses
        if address["id"] == first_address["id"]
    )

    second_address_data = next(
        address
        for address in addresses
        if address["id"] == second_address["id"]
    )

    # Verify only second address is default
    assert first_address_data["is_default"] is False
    assert second_address_data["is_default"] is True

# ============================================================
# DEFAULT ADDRESS REASSIGNMENT AFTER DELETION
# ============================================================

def test_default_address_reassigned_after_deletion():
    unique_id = uuid4().hex[:8]

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    customer_response = client.post(
        "/customers",
        json={
            "name": "Delete Address User",
            "email": f"delete_address_{unique_id}@example.com",
            "phone": f"7{uuid4().int % 1000000000:09d}",
        },
    )

    assert customer_response.status_code == 201

    customer_id = customer_response.json()["id"]

    # --------------------------------------------------------
    # CREATE FIRST ADDRESS
    # First address automatically becomes default
    # --------------------------------------------------------

    first_address_response = client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "address_line": "First Delete Test Street",
            "city": "Hyderabad",
            "pincode": "500001",
            "address_type": "Home",
            "is_default": False,
        },
    )

    assert first_address_response.status_code == 201

    first_address = first_address_response.json()

    assert first_address["is_default"] is True

    # --------------------------------------------------------
    # CREATE SECOND ADDRESS
    # --------------------------------------------------------

    second_address_response = client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "address_line": "Second Delete Test Street",
            "city": "Bengaluru",
            "pincode": "560001",
            "address_type": "Work",
            "is_default": False,
        },
    )

    assert second_address_response.status_code == 201

    second_address = second_address_response.json()

    assert second_address["is_default"] is False

    # --------------------------------------------------------
    # DELETE THE DEFAULT ADDRESS
    # --------------------------------------------------------

    delete_response = client.delete(
        f"/addresses/{first_address['id']}"
    )

    assert delete_response.status_code == 200

    assert (
        delete_response.json()["message"]
        == "Address deleted successfully"
    )

    # --------------------------------------------------------
    # GET REMAINING ADDRESSES
    # --------------------------------------------------------

    addresses_response = client.get(
        f"/customers/{customer_id}/addresses"
    )

    assert addresses_response.status_code == 200

    addresses = addresses_response.json()

    # Only one address should remain
    assert len(addresses) == 1

    # Remaining address should automatically become default
    assert addresses[0]["id"] == second_address["id"]
    assert addresses[0]["is_default"] is True

# ============================================================
# DELETE ADDRESS - NOT FOUND
# ============================================================

def test_delete_address_not_found():
    response = client.delete(
        "/addresses/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"

# ============================================================
# DELETE NON-DEFAULT ADDRESS
# ============================================================

def test_delete_non_default_address():
    unique_id = uuid4().hex[:8]

    # Create customer
    customer_response = client.post(
        "/customers",
        json={
            "name": "Non Default Delete User",
            "email": f"non_default_{unique_id}@example.com",
            "phone": f"6{uuid4().int % 1000000000:09d}",
        },
    )

    assert customer_response.status_code == 201

    customer_id = customer_response.json()["id"]

    # Create first address
    # First address automatically becomes default
    first_address_response = client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "address_line": "Default Address Street",
            "city": "Hyderabad",
            "pincode": "500001",
            "address_type": "Home",
            "is_default": False,
        },
    )

    assert first_address_response.status_code == 201

    first_address = first_address_response.json()

    assert first_address["is_default"] is True

    # Create second non-default address
    second_address_response = client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "address_line": "Non Default Address Street",
            "city": "Bengaluru",
            "pincode": "560001",
            "address_type": "Work",
            "is_default": False,
        },
    )

    assert second_address_response.status_code == 201

    second_address = second_address_response.json()

    assert second_address["is_default"] is False

    # Delete the non-default address
    delete_response = client.delete(
        f"/addresses/{second_address['id']}"
    )

    assert delete_response.status_code == 200

    assert (
        delete_response.json()["message"]
        == "Address deleted successfully"
    )

    # Verify the default address still exists
    addresses_response = client.get(
        f"/customers/{customer_id}/addresses"
    )

    assert addresses_response.status_code == 200

    addresses = addresses_response.json()

    assert len(addresses) == 1
    assert addresses[0]["id"] == first_address["id"]
    assert addresses[0]["is_default"] is True