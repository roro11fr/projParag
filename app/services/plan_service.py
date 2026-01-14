import logging
from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from app.domain.models.plan import Plan
from app.domain.repositories.plan_repo import PlanRepo
from app.domain.schemas.plan_schema import PlanCreate, PlanUpdate
from app.domain.exceptions import PlanNotFound, PlanInactive, PlanNameAlreadyExists

logger = logging.getLogger(__name__)


class PlanService:
    def __init__(self, repo: PlanRepo):
        self.repo = repo

    # ---------- PUBLIC / USER ----------

    async def list_active(self) -> list[Plan]:
        logger.info("plan.list_active")
        return await self.repo.list_active()

    async def get_active_by_id(self, plan_id: int) -> Plan:
        logger.info(f"plan.get_active | id={plan_id}")

        plan = await self.repo.get_by_id(plan_id)
        if not plan:
            logger.warning(f"plan.not_found | id={plan_id}")
            raise PlanNotFound()

        if not plan.is_active:
            logger.warning(f"plan.inactive | id={plan_id}")
            raise PlanInactive()

        return plan

    # ---------- ADMIN ----------

    async def list_all(self) -> list[Plan]:
        logger.info("plan.list_all")
        return await self.repo.list_all()

    async def get_by_id(self, plan_id: int) -> Plan:
        logger.info(f"plan.get | id={plan_id}")

        plan = await self.repo.get_by_id(plan_id)
        if not plan:
            logger.warning(f"plan.not_found | id={plan_id}")
            raise PlanNotFound()

        return plan

    async def create_plan(self, data: PlanCreate) -> Plan:
        logger.info(f"plan.create | name={data.name} period={data.billing_period} active={data.is_active}")

        existing = await self.repo.get_by_name(data.name)
        if existing:
            logger.warning(f"plan.create conflict name | name={data.name}")
            raise PlanNameAlreadyExists()

        plan = Plan(
            id=None,
            name=data.name,
            price=Decimal(str(data.price)),
            billing_period=data.billing_period,
            is_active=data.is_active,
            currency=data.currency,
        )

        try:
            created = await self.repo.create(plan)
        except IntegrityError:
            logger.warning(f"plan.create integrity_conflict | name={data.name}")
            raise PlanNameAlreadyExists()

        logger.info(f"plan.created | id={getattr(created, 'id', None)} name={created.name}")
        return created

    async def update_plan(self, plan_id: int, data: PlanUpdate) -> Plan:
        logger.info(f"plan.update | id={plan_id}")

        current = await self.repo.get_by_id(plan_id)
        if not current:
            logger.warning(f"plan.not_found | id={plan_id}")
            raise PlanNotFound()

        payload = data.model_dump(exclude_unset=True)

        if "name" in payload and payload["name"] is not None:
            existing = await self.repo.get_by_name(payload["name"])
            if existing and existing.id != plan_id:
                logger.warning(f"plan.update conflict name | id={plan_id} name={payload['name']}")
                raise PlanNameAlreadyExists()

        try:
            updated = await self.repo.update(plan_id, payload)
        except IntegrityError:
            logger.warning(f"plan.update integrity_conflict | id={plan_id} payload_name={payload.get('name')}")
            raise PlanNameAlreadyExists()

        if not updated:
            logger.warning(f"plan.not_found | id={plan_id}")
            raise PlanNotFound()

        logger.info(f"plan.updated | id={plan_id}")
        return updated

    async def delete_plan(self, plan_id: int) -> None:
        logger.info(f"plan.delete | id={plan_id}")

        ok = await self.repo.delete(plan_id)
        if not ok:
            logger.warning(f"plan.not_found | id={plan_id}")
            raise PlanNotFound()

        logger.info(f"plan.deleted | id={plan_id}")