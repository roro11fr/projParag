import logging
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

from app.core.cache import SimpleCache
from app.domain.models.plan import Plan
from app.domain.repositories.plan_repo import PlanRepo
from app.domain.schemas.plan_schema import PlanCreate, PlanUpdate
from app.domain.exceptions import PlanNotFound, PlanInactive, PlanNameAlreadyExists

logger = logging.getLogger(__name__)


class PlanService:
    def __init__(self, repo: PlanRepo, cache: SimpleCache):
        self.repo = repo
        self.cache = cache

    # ---------- PUBLIC / USER ----------

    async def list_active(self) -> list[Plan]:
        key = "plan:active_list"
        cached = self.cache.get(key)
        if cached is not None:
            logger.info("plan.list_active | cache_hit")
            return cached

        logger.info("plan.list_active | cache_miss")
        plans = await self.repo.list_active()
        self.cache.set(key, plans, ttl_seconds=60)
        return plans

    async def get_active_by_id(self, plan_id: int) -> Plan:
        key = f"plan:active:{plan_id}"
        cached = self.cache.get(key)
        if cached is not None:
            logger.info(f"plan.get_active | id={plan_id} | cache_hit")
            return cached

        logger.info(f"plan.get_active | id={plan_id} | cache_miss")
        plan = await self.repo.get_by_id(plan_id)
        if not plan:
            logger.warning(f"plan.not_found | id={plan_id}")
            raise PlanNotFound()

        if not plan.is_active:
            logger.warning(f"plan.inactive | id={plan_id}")
            raise PlanInactive()

        self.cache.set(key, plan, ttl_seconds=60)
        return plan

    # ---------- ADMIN ----------

    async def list_all(self) -> list[Plan]:
        key = "plan:all_list"
        cached = self.cache.get(key)
        if cached is not None:
            logger.info("plan.list_all | cache_hit")
            return cached

        logger.info("plan.list_all | cache_miss")
        plans = await self.repo.list_all()
        self.cache.set(key, plans, ttl_seconds=30)
        return plans

    async def get_by_id(self, plan_id: int) -> Plan:
        key = f"plan:{plan_id}"
        cached = self.cache.get(key)
        if cached is not None:
            logger.info(f"plan.get | id={plan_id} | cache_hit")
            return cached

        logger.info(f"plan.get | id={plan_id} | cache_miss")
        plan = await self.repo.get_by_id(plan_id)
        if not plan:
            logger.warning(f"plan.not_found | id={plan_id}")
            raise PlanNotFound()

        self.cache.set(key, plan, ttl_seconds=60)
        return plan

    def _invalidate_plan_cache(self, plan_id: int | None = None) -> None:
        # listele
        self.cache.delete("plan:active_list")
        self.cache.delete("plan:all_list")
        # plan by id
        if plan_id is not None:
            self.cache.delete(f"plan:{plan_id}")
            self.cache.delete(f"plan:active:{plan_id}")

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

        self._invalidate_plan_cache(plan_id=created.id)
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

        self._invalidate_plan_cache(plan_id=plan_id)
        return updated

    async def delete_plan(self, plan_id: int) -> None:
        logger.info(f"plan.delete | id={plan_id}")

        ok = await self.repo.delete(plan_id)
        if not ok:
            logger.warning(f"plan.not_found | id={plan_id}")
            raise PlanNotFound()

        self._invalidate_plan_cache(plan_id=plan_id)
