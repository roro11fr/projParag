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


class SubscriptionService:
    def __init__(self, repo: SubscriptionRepo, plan_repo: PlanRepo):
        self.repo = repo
        self.plan_repo = plan_repo

    @staticmethod
    def _validate_dates(start_date: date, end_date: date) -> None:
        if end_date < start_date:
            raise InvalidSubscriptionDates("end_date must be >= start_date")

    async def create_for_client(self, client_id: int, data: SubscriptionCreate):
        self._validate_dates(data.start_date, data.end_date)

        plan = await self.plan_repo.get_by_id(data.plan_id)
        if not plan:
            raise PlanNotFound()

        if not plan.is_active:
            raise PlanInactive()

        return await self.repo.create(
            client_id,
            plan_id=plan.id,
            start_date=data.start_date,
            end_date=data.end_date,
            status=data.status,
            price_snapshot=plan.price,
            currency_snapshot=plan.currency,
        )

    async def list_for_client(self, client_id: int):
        return await self.repo.list_by_client(client_id)

    async def patch(self, sub_id: int, data: SubscriptionPatch):
        current = await self.repo.get_by_id(sub_id)
        if not current:
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
            raise SubscriptionNotFound()

        return updated

    async def renew(self, sub_id: int, months: int):
        current = await self.repo.get_by_id(sub_id)
        if not current:
            raise SubscriptionNotFound()

        new_end = current.end_date + relativedelta(months=months)

        updated = await self.repo.update_field(
            sub_id,
            status=SubscriptionStatus.ACTIVE,
            end_date=new_end,
        )
        if not updated:
            raise SubscriptionNotFound()
        return updated

    async def expire(self, sub_id: int, today: date | None = None):
        today = today or date.today()

        current = await self.repo.get_by_id(sub_id)
        if not current:
            raise SubscriptionNotFound()

        if current.end_date < today and current.status != SubscriptionStatus.EXPIRED:
            updated = await self.repo.update_field(sub_id, status=SubscriptionStatus.EXPIRED)
            if not updated:
                raise SubscriptionNotFound()
            return updated

        return current

    async def delete(self, sub_id: int) -> None:
        deleted = await self.repo.delete(sub_id)
        if not deleted:
            raise SubscriptionNotFound()