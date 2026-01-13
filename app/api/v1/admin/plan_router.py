from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.plan_repository import PlanRepository
from app.services.plan_service import PlanService
from app.domain.schemas.plan_schema import PlanCreate, PlanUpdate, PlanRead

router = APIRouter(prefix="/admin/plans", tags=["admin-plans"])


def get_plan_service(db: AsyncSession = Depends(get_db)) -> PlanService:
    return PlanService(PlanRepository(db))


@router.get("", response_model=list[PlanRead])
async def list_plans(service: PlanService = Depends(get_plan_service)):
    return await service.list_all()


@router.get("/{plan_id}", response_model=PlanRead)
async def get_plan(plan_id: int, service: PlanService = Depends(get_plan_service)):
    return await service.get_by_id(plan_id)


@router.post("", response_model=PlanRead, status_code=status.HTTP_201_CREATED)
async def create_plan(data: PlanCreate, service: PlanService = Depends(get_plan_service)):
    return await service.create_plan(data)


@router.put("/{plan_id}", response_model=PlanRead)
async def update_plan(plan_id: int, data: PlanUpdate, service: PlanService = Depends(get_plan_service)):
    return await service.update_plan(plan_id, data)


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(plan_id: int, service: PlanService = Depends(get_plan_service)):
    await service.delete_plan(plan_id)
    return None