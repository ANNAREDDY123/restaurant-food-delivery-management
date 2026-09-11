from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.delivery import (
    DeliveryPartnerCreate,
    DeliveryPartnerStatusUpdate,
    DeliveryPartnerResponse,
    AssignDriverRequest,
)

from app.services.delivery_service import (
    create_delivery_partner,
    get_delivery_partners,
    update_delivery_partner_status,
    assign_driver_to_order,
)

from app.services.notification_service import (
    notify_driver_assigned,
)


router = APIRouter(
    prefix="/delivery-partners",
    tags=["Delivery Partners"],
)


# ============================================================
# CREATE DELIVERY PARTNER
# ============================================================

@router.post(
    "",
    response_model=DeliveryPartnerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_delivery_partner(
    partner_data: DeliveryPartnerCreate,
    db: Session = Depends(get_db),
):
    return create_delivery_partner(
        db=db,
        partner_data=partner_data,
    )


# ============================================================
# GET DELIVERY PARTNERS
# ============================================================

@router.get(
    "",
    response_model=list[DeliveryPartnerResponse],
)
def get_all_delivery_partners(
    db: Session = Depends(get_db),
):
    return get_delivery_partners(
        db=db,
    )


# ============================================================
# UPDATE DELIVERY PARTNER STATUS
# ============================================================

@router.put(
    "/{delivery_partner_id}/status",
    response_model=DeliveryPartnerResponse,
)
def update_partner_status(
    delivery_partner_id: int,
    status_data: DeliveryPartnerStatusUpdate,
    db: Session = Depends(get_db),
):
    return update_delivery_partner_status(
        db=db,
        delivery_partner_id=delivery_partner_id,
        availability_status=(
            status_data.availability_status
        ),
        current_location=(
            status_data.current_location
        ),
    )


# ============================================================
# ASSIGN DRIVER TO ORDER
# ============================================================

@router.post(
    "/orders/{order_id}/assign-driver",
)
def assign_driver(
    order_id: int,
    driver_data: AssignDriverRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    order = assign_driver_to_order(
        db=db,
        order_id=order_id,
        delivery_partner_id=(
            driver_data.delivery_partner_id
        ),
    )

    # Send driver assignment notification
    # in the background
    background_tasks.add_task(
        notify_driver_assigned,
        order.id,
        str(order.delivery_partner_id),
    )

    return {
        "message": "Driver assigned successfully",
        "order_id": order.id,
        "delivery_partner_id": (
            order.delivery_partner_id
        ),
    }