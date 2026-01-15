from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.plan_repository import PlanRepository
from app.infrastructure.repositories.subscription_repository import SubscriptionRepository
from app.services.subscription_service import SubscriptionService
from app.domain.schemas.subscription_schema import (
    SubscriptionCreate,
    SubscriptionRead,
    RenewRequest,
)

router = APIRouter(tags=["subscriptions"])


def get_service(db: AsyncSession = Depends(get_db)) -> SubscriptionService:
    return SubscriptionService(SubscriptionRepository(db), PlanRepository(db))


@router.post(
    "/clients/{client_id}/subscriptions",
    response_model=SubscriptionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription(
    client_id: int,
    payload: SubscriptionCreate,
    service: SubscriptionService = Depends(get_service),
):
    return await service.create_for_client(client_id, payload)


@router.get(
    "/clients/{client_id}/subscriptions",
    response_model=list[SubscriptionRead],
)
async def list_subscriptions(
    client_id: int,
    service: SubscriptionService = Depends(get_service),
):
    return await service.list_for_client(client_id)


@router.post(
    "/subscriptions/{sub_id}/renew",
    response_model=SubscriptionRead,
)
async def renew_subscription(
    sub_id: int,
    payload: RenewRequest,
    service: SubscriptionService = Depends(get_service),
):
    return await service.renew(sub_id, months=payload.months)


@router.post(
    "/subscriptions/{sub_id}/expire",
    response_model=SubscriptionRead,
)
async def expire_subscription(
    sub_id: int,
    service: SubscriptionService = Depends(get_service),
):
    return await service.expire(sub_id)