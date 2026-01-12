from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.plan import Plan
from app.infrastructure.orm.plan_orm import PlanORM
from app.infrastructure.mappers.plan_mapper import to_domain


class PlanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_active(self) -> list[Plan]:
        res = await self.db.execute(
            select(PlanORM).where(PlanORM.is_active.is_(True))
        )
        rows = res.scalars().all()
        return [to_domain(row) for row in rows]

    async def get_by_id(self, plan_id: int) -> Plan | None:
        stmt = select(PlanORM).where(
            (PlanORM.id == plan_id) & (PlanORM.is_active.is_(True))
        )
        res = await self.db.execute(stmt)
        row = res.scalar_one_or_none()
        return to_domain(row) if row else None