from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.address import Address

from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    AddressCreate,
    AddressResponse,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


# ============================================================
# CREATE CUSTOMER
# ============================================================

@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
):
    existing_customer = (
        db.query(Customer)
        .filter(Customer.email == customer.email)
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this email already exists",
        )

    existing_phone = (
        db.query(Customer)
        .filter(Customer.phone == customer.phone)
        .first()
    )

    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this phone already exists",
        )

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# ============================================================
# GET ALL CUSTOMERS
# SEARCH / FILTER / PAGINATION / SORTING
# ============================================================

@router.get(
    "",
    response_model=list[CustomerResponse],
)
def get_customers(
    name: str | None = None,
    email: str | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
):

    # Validate pagination
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be greater than 0",
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100",
        )

    query = db.query(Customer)

    # Filter by name
    if name:
        query = query.filter(
            Customer.name.ilike(
                f"%{name}%"
            )
        )

    # Filter by email
    if email:
        query = query.filter(
            Customer.email.ilike(
                f"%{email}%"
            )
        )

    # Allowed sorting fields
    allowed_sort_fields = {
        "id": Customer.id,
        "name": Customer.name,
        "email": Customer.email,
        "phone": Customer.phone,
        "created_at": Customer.created_at,
    }

    sort_column = allowed_sort_fields.get(
        sort_by
    )

    if not sort_column:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sort_by field",
        )

    if sort_order.lower() == "asc":
        query = query.order_by(
            sort_column.asc()
        )

    elif sort_order.lower() == "desc":
        query = query.order_by(
            sort_column.desc()
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sort_order must be asc or desc",
        )

    # Pagination
    offset = (
        page - 1
    ) * limit

    customers = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return customers


# ============================================================
# GET CUSTOMER BY ID
# ============================================================

@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


# ============================================================
# UPDATE CUSTOMER
# ============================================================

@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    update_data = customer_data.model_dump(
        exclude_unset=True
    )

    # Check duplicate email
    if "email" in update_data:
        existing_customer = (
            db.query(Customer)
            .filter(
                Customer.email == update_data["email"],
                Customer.id != customer_id,
            )
            .first()
        )

        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Customer with this email already exists"
                ),
            )

    # Check duplicate phone
    if "phone" in update_data:
        existing_phone = (
            db.query(Customer)
            .filter(
                Customer.phone == update_data["phone"],
                Customer.id != customer_id,
            )
            .first()
        )

        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Customer with this phone already exists"
                ),
            )

    # Update fields
    for field, value in update_data.items():
        setattr(
            customer,
            field,
            value,
        )

    db.commit()
    db.refresh(customer)

    return customer


# ============================================================
# ADD CUSTOMER ADDRESS
# ============================================================

@router.post(
    "/{customer_id}/addresses",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_address(
    customer_id: int,
    address: AddressCreate,
    db: Session = Depends(get_db),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    # Check existing addresses
    existing_addresses = (
        db.query(Address)
        .filter(Address.customer_id == customer_id)
        .count()
    )

    # First address becomes default automatically
    if existing_addresses == 0:
        is_default = True
    else:
        is_default = address.is_default

    # Remove default status from other addresses
    if is_default:
        (
            db.query(Address)
            .filter(Address.customer_id == customer_id)
            .update(
                {"is_default": False},
                synchronize_session=False,
            )
        )

    new_address = Address(
        customer_id=customer_id,
        address_line=address.address_line,
        city=address.city,
        pincode=address.pincode,
        latitude=address.latitude,
        longitude=address.longitude,
        address_type=address.address_type,
        is_default=is_default,
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return new_address


# ============================================================
# GET CUSTOMER ADDRESSES
# ============================================================

@router.get(
    "/{customer_id}/addresses",
    response_model=list[AddressResponse],
)
def get_customer_addresses(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    addresses = (
        db.query(Address)
        .filter(Address.customer_id == customer_id)
        .all()
    )

    return addresses