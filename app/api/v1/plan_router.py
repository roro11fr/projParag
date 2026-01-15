from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.container import cache
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.plan_repository import PlanRepository
from app.services.plan_service import PlanService
from app.domain.schemas.plan_schema import PlanRead

router = APIRouter(prefix="/plans", tags=["plans"])


def get_plan_service(db: AsyncSession = Depends(get_db)) -> PlanService:
    repo = PlanRepository(db)
    return PlanService(repo, cache)


@router.get("", response_model=list[PlanRead])
async def list_plans(service: PlanService = Depends(get_plan_service)):
    return await service.list_active()