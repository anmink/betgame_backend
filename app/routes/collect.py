from datetime import UTC, datetime

from fastapi import APIRouter, Depends

from app.core.dependencies import get_collect_service
from app.core.security import get_current_user
from app.schemas.collect import CollectResponse
from app.services.collect_service import CollectService

router = APIRouter(prefix="/collect", tags=["collect"])


@router.post("/", response_model=CollectResponse)
def collect(
    current_user: dict = Depends(get_current_user),
    service: CollectService = Depends(get_collect_service),
):
    return service.collect(current_user["id"], datetime.now(UTC))
