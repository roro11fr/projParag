from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.plan_repository import PlanRepository
from app.infrastructure.repositories.subscription_repository import SubscriptionRepository
from app.services.subscription_service import SubscriptionService
from app.domain.schemas.subscription_schema import SubscriptionRead, SubscriptionPatch

router = APIRouter(prefix="/admin/subscriptions", tags=["admin-subscriptions"])


def get_service(db: AsyncSession = Depends(get_db)) -> SubscriptionService:
    return SubscriptionService(SubscriptionRepository(db), PlanRepository(db))


@router.patch("/{sub_id}", response_model=SubscriptionRead)
async def patch_subscription(
    sub_id: int,
    payload: SubscriptionPatch,
    service: SubscriptionService = Depends(get_service),
):
    return await service.patch(sub_id, payload)


@router.delete("/{sub_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(
    sub_id: int,
    svc: SubscriptionService = Depends(get_service),
):
    await svc.delete(sub_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)