from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.dashboard import (
    RestaurantDashboardResponse,
)

from app.services.dashboard_service import (
    get_restaurant_dashboard,
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Restaurant Dashboard"],
)


@router.get(
    "/restaurants/{restaurant_id}",
    response_model=RestaurantDashboardResponse,
)
def restaurant_dashboard(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    dashboard_data = get_restaurant_dashboard(
        db=db,
        restaurant_id=restaurant_id,
    )

    if dashboard_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    return dashboard_data