from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.admin_analytics import (
    AdminAnalyticsResponse,
)

from app.services.admin_analytics_service import (
    get_admin_analytics,
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin Analytics"],
)


@router.get(
    "/analytics",
    response_model=AdminAnalyticsResponse,
)
def admin_analytics(
    db: Session = Depends(get_db),
):
    return get_admin_analytics(
        db=db,
    )