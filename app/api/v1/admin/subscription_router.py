from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import SubscriptionNotFound, InvalidSubscriptionDates
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.plan_repository import PlanRepository
from app.infrastructure.repositories.subscription_repository import SubscriptionRepository
from app.services.subscription_service import SubscriptionService
from app.domain.schemas.subscription_schema import SubscriptionRead, SubscriptionPatch

router = APIRouter(prefix="/admin/subscriptions" ,tags=["admin-subscriptions"])


def get_service(db: AsyncSession = Depends(get_db)) -> SubscriptionService:
    sub_repo = SubscriptionRepository(db)
    plan_repo = PlanRepository(db)
    return SubscriptionService(sub_repo, plan_repo)


@router.patch(
    "/subscriptions/{id}",
    response_model=SubscriptionRead,
)
async def patch_subscription(id: int, payload: SubscriptionPatch, service: SubscriptionService = Depends(get_service)):
    try:
        return await service.patch(id, payload)
    except SubscriptionNotFound:
        raise HTTPException(status_code=404, detail="Subscription not found")
    except InvalidSubscriptionDates as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/subscriptions/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(
    sub_id: int,
    svc: SubscriptionService = Depends(get_service),
) -> None:
    await svc.delete(sub_id)
    return None