from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.plan import Plan
from app.infrastructure.orm.plan_orm import PlanORM
from app.infrastructure.mappers.plan_mapper import to_domain


class PlanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------- READ ----------

    async def list_active(self) -> list[Plan]:
        res = await self.db.execute(
            select(PlanORM).where(PlanORM.is_active.is_(True))
        )
        rows = res.scalars().all()
        return [to_domain(row) for row in rows]

    async def list_all(self) -> list[Plan]:
        res = await self.db.execute(select(PlanORM))
        rows = res.scalars().all()
        return [to_domain(row) for row in rows]

    async def get_by_id(self, plan_id: int) -> Plan | None:
        res = await self.db.execute(
            select(PlanORM).where(PlanORM.id == plan_id)
        )
        row = res.scalar_one_or_none()
        return to_domain(row) if row else None

    async def get_by_name(self, name: str) -> Plan | None:
        res = await self.db.execute(
            select(PlanORM).where(PlanORM.name == name)
        )
        row = res.scalar_one_or_none()
        return to_domain(row) if row else None

    # ---------- WRITE ----------

    async def create(self, plan: Plan) -> Plan:
        orm = PlanORM(
            name=plan.name,
            price=plan.price,
            currency=plan.currency,
            billing_period=plan.billing_period,
            is_active=plan.is_active,
        )
        self.db.add(orm)
        await self.db.commit()
        await self.db.refresh(orm)
        return to_domain(orm)

    async def update(self, plan_id: int, data: dict) -> Plan | None:
        res = await self.db.execute(
            select(PlanORM).where(PlanORM.id == plan_id)
        )
        orm = res.scalar_one_or_none()
        if not orm:
            return None

        if data.get("name") is not None:
            orm.name = data["name"]
        if data.get("price") is not None:
            orm.price = data["price"]
        if data.get("billing_period") is not None:
            orm.billing_period = data["billing_period"]
        if data.get("is_active") is not None:
            orm.is_active = data["is_active"]

        await self.db.commit()
        await self.db.refresh(orm)
        return to_domain(orm)

    async def delete(self, plan_id: int) -> bool:
        """
        Soft delete: is_active = False
        """
        res = await self.db.execute(
            select(PlanORM).where(PlanORM.id == plan_id)
        )
        orm = res.scalar_one_or_none()
        if not orm:
            return False

        orm.is_active = False
        await self.db.commit()
        return True