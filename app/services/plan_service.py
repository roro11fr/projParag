from sqlalchemy.exc import IntegrityError

from app.domain.models.plan import Plan
from app.domain.schemas.plan_schema import PlanCreate, PlanUpdate
from app.domain.exceptions import PlanNotFound, PlanInactive, PlanNameAlreadyExists
from app.infrastructure.repositories.plan_repository import PlanRepository


class PlanService:
    def __init__(self, repo: PlanRepository):
        self.repo = repo

    # ---------- PUBLIC / USER ----------

    async def list_active(self) -> list[Plan]:
        return await self.repo.list_active()

    async def get_active_by_id(self, plan_id: int) -> Plan:

        plan = await self.repo.get_by_id(plan_id)
        if not plan:
            raise PlanNotFound()
        if not plan.is_active:
            raise PlanInactive()
        return plan

    # ---------- ADMIN ----------

    async def list_all(self) -> list[Plan]:
        return await self.repo.list_all()

    async def get_by_id(self, plan_id: int) -> Plan:
        plan = await self.repo.get_by_id(plan_id)
        if not plan:
            raise PlanNotFound()
        return plan

    async def create_plan(self, data: PlanCreate) -> Plan:
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise PlanNameAlreadyExists()

        plan = Plan(
            id=None,
            name=data.name,
            price=data.price,
            billing_period=data.billing_period,
            is_active=data.is_active,
            currency=data.currency,
        )

        try:
            return await self.repo.create(plan)
        except IntegrityError:
            raise PlanNameAlreadyExists()

    async def update_plan(self, plan_id: int, data: PlanUpdate) -> Plan:
        current = await self.repo.get_by_id(plan_id)
        if not current:
            raise PlanNotFound()

        payload = data.model_dump(exclude_unset=True)

        if "name" in payload and payload["name"] is not None:
            existing = await self.repo.get_by_name(payload["name"])
            if existing and existing.id != plan_id:
                raise PlanNameAlreadyExists()

        try:
            updated = await self.repo.update(plan_id, payload)
        except IntegrityError:
            raise PlanNameAlreadyExists()

        if not updated:
            raise PlanNotFound()
        return updated

    async def delete_plan(self, plan_id: int) -> None:
        ok = await self.repo.delete(plan_id)
        if not ok:
            raise PlanNotFound()
