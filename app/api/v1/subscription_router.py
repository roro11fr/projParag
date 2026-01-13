from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.plan_repository import PlanRepository
from app.infrastructure.repositories.subscription_repository import SubscriptionRepository
from app.services.subscription_service import SubscriptionService
from app.domain.schemas.subscription_schema import (
    SubscriptionCreate, SubscriptionPatch, SubscriptionRead, RenewRequest
)
from app.domain.exceptions import SubscriptionNotFound, InvalidSubscriptionDates

router = APIRouter(tags=["subscriptions"])


def get_service(db: AsyncSession = Depends(get_db)) -> SubscriptionService:
    sub_repo = SubscriptionRepository(db)
    plan_repo = PlanRepository(db)
    return SubscriptionService(sub_repo, plan_repo)


@router.post(
    "/clients/{client_id}/subscriptions",
    response_model=SubscriptionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription(client_id: int, payload: SubscriptionCreate, service: SubscriptionService = Depends(get_service)):
    try:
        return await service.create_for_client(client_id, payload)
    except InvalidSubscriptionDates as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/clients/{client_id}/subscriptions",
    response_model=list[SubscriptionRead],
)
async def list_subscriptions(client_id: int, service: SubscriptionService = Depends(get_service)):
    return await service.list_for_client(client_id)


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


@router.post(
    "/subscriptions/{id}/renew",
    response_model=SubscriptionRead,
)
async def renew_subscription(id: int, payload: RenewRequest, service: SubscriptionService = Depends(get_service)):
    try:
        return await service.renew(id, months=payload.months)
    except SubscriptionNotFound:
        raise HTTPException(status_code=404, detail="Subscription not found")


@router.post(
    "/subscriptions/{id}/expire",
    response_model=SubscriptionRead,
)
async def expire_subscription(id: int, service: SubscriptionService = Depends(get_service)):
    try:
        return await service.expire(id, today=date.today())
    except SubscriptionNotFound:
        raise HTTPException(status_code=404, detail="Subscription not found")