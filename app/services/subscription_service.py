import logging
from datetime import date

from dateutil.relativedelta import relativedelta

from app.domain.exceptions import (
    SubscriptionNotFound,
    InvalidSubscriptionDates,
    PlanNotFound,
    PlanInactive,
)
from app.domain.models.subscription import SubscriptionStatus
from app.domain.repositories.plan_repo import PlanRepo
from app.domain.repositories.subscription_repo import SubscriptionRepo
from app.domain.schemas.subscription_schema import SubscriptionCreate, SubscriptionPatch

logger = logging.getLogger(__name__)


class SubscriptionService:
    def __init__(self, repo: SubscriptionRepo, plan_repo: PlanRepo):
        self.repo = repo
        self.plan_repo = plan_repo

    @staticmethod
    def _validate_dates(start_date: date, end_date: date) -> None:
        if end_date < start_date:
            raise InvalidSubscriptionDates("end_date must be >= start_date")

    async def create_for_client(self, client_id: int, data: SubscriptionCreate):
        logger.info(f"subscription.create | client_id={client_id} plan_id={data.plan_id}")

        self._validate_dates(data.start_date, data.end_date)

        plan = await self.plan_repo.get_by_id(data.plan_id)
        if not plan:
            logger.warning(f"subscription.create plan_not_found | plan_id={data.plan_id}")
            raise PlanNotFound()

        if not plan.is_active:
            logger.warning(f"subscription.create plan_inactive | plan_id={plan.id}")
            raise PlanInactive()

        created = await self.repo.create(
            client_id,
            plan_id=plan.id,
            start_date=data.start_date,
            end_date=data.end_date,
            status=data.status,
            price_snapshot=plan.price,
            currency_snapshot=plan.currency,
        )

        logger.info(f"subscription.created | id={getattr(created, 'id', None)} client_id={client_id}")
        return created

    async def list_for_client(self, client_id: int):
        logger.info(f"subscription.list | client_id={client_id}")
        return await self.repo.list_by_client(client_id)

    async def patch(self, sub_id: int, data: SubscriptionPatch):
        logger.info(f"subscription.patch | id={sub_id}")

        current = await self.repo.get_by_id(sub_id)
        if not current:
            logger.warning(f"subscription.not_found | id={sub_id}")
            raise SubscriptionNotFound()

        new_start = data.start_date if data.start_date is not None else current.start_date
        new_end = data.end_date if data.end_date is not None else current.end_date
        self._validate_dates(new_start, new_end)

        updated = await self.repo.update_field(
            sub_id,
            status=data.status,
            start_date=data.start_date,
            end_date=data.end_date,
        )
        if not updated:
            logger.warning(f"subscription.not_found | id={sub_id}")
            raise SubscriptionNotFound()

        logger.info(f"subscription.patched | id={sub_id}")
        return updated

    async def renew(self, sub_id: int, months: int):
        logger.info(f"subscription.renew | id={sub_id} months={months}")

        current = await self.repo.get_by_id(sub_id)
        if not current:
            logger.warning(f"subscription.not_found | id={sub_id}")
            raise SubscriptionNotFound()

        new_end = current.end_date + relativedelta(months=months)

        updated = await self.repo.update_field(
            sub_id,
            status=SubscriptionStatus.ACTIVE,
            end_date=new_end,
        )
        if not updated:
            logger.warning(f"subscription.not_found | id={sub_id}")
            raise SubscriptionNotFound()

        logger.info(f"subscription.renewed | id={sub_id} new_end={new_end}")
        return updated

    async def expire(self, sub_id: int, today: date | None = None):
        today = today or date.today()
        logger.info(f"subscription.expire | id={sub_id} today={today}")

        current = await self.repo.get_by_id(sub_id)
        if not current:
            logger.warning(f"subscription.not_found | id={sub_id}")
            raise SubscriptionNotFound()

        if current.status == SubscriptionStatus.EXPIRED:
            logger.info(f"subscription.already_expired | id={sub_id}")
            return current

        updated = await self.repo.update_field(
            sub_id,
            status=SubscriptionStatus.EXPIRED,
            end_date=today,
        )
        if not updated:
            logger.warning(f"subscription.not_found | id={sub_id}")
            raise SubscriptionNotFound()

        logger.info(f"subscription.expired | id={sub_id}")
        return updated

    async def delete(self, sub_id: int) -> None:
        logger.info(f"subscription.delete | id={sub_id}")

        deleted = await self.repo.delete(sub_id)
        if not deleted:
            logger.warning(f"subscription.not_found | id={sub_id}")
            raise SubscriptionNotFound()

        logger.info(f"subscription.deleted | id={sub_id}")