from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.address import Address
from app.schemas.customer import (
    AddressUpdate,
    AddressResponse,
)


router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"],
)


# ============================================================
# UPDATE ADDRESS
# ============================================================

@router.put(
    "/{address_id}",
    response_model=AddressResponse,
)
def update_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
):
    address = (
        db.query(Address)
        .filter(Address.id == address_id)
        .first()
    )

    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )

    update_data = address_data.model_dump(
        exclude_unset=True
    )

    # If making this address default,
    # remove default status from other addresses.
    if update_data.get("is_default") is True:
        (
            db.query(Address)
            .filter(
                Address.customer_id == address.customer_id,
                Address.id != address_id,
            )
            .update(
                {"is_default": False},
                synchronize_session=False,
            )
        )

    for field, value in update_data.items():
        setattr(address, field, value)

    db.commit()
    db.refresh(address)

    return address


# ============================================================
# DELETE ADDRESS
# ============================================================

@router.delete(
    "/{address_id}",
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
):
    address = (
        db.query(Address)
        .filter(Address.id == address_id)
        .first()
    )

    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )

    customer_id = address.customer_id
    was_default = address.is_default

    db.delete(address)
    db.commit()

    # If the deleted address was the default address,
    # make another remaining address the default.
    if was_default:
        remaining_address = (
            db.query(Address)
            .filter(
                Address.customer_id == customer_id
            )
            .first()
        )

        if remaining_address:
            remaining_address.is_default = True
            db.commit()

    return {
        "message": "Address deleted successfully"
    }