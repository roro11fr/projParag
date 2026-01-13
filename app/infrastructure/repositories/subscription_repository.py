from datetime import date
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.subscription import Subscription, SubscriptionStatus
from app.infrastructure.mappers.subscription_mapper import to_domain
from app.infrastructure.orm.subscription_orm import SubscriptionORM
from app.domain.repositories.subscription_repo import SubscriptionRepo

class SubscriptionRepository(SubscriptionRepo):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        client_id: int,
        *,
        start_date: date,
        end_date: date,
        status: SubscriptionStatus,
        plan_id: int,
        price_snapshot: Decimal,
        currency_snapshot: str,
    ) -> Subscription:
        obj = SubscriptionORM(
            client_id=client_id,
            plan_id = plan_id,
            start_date=start_date,
            end_date=end_date,
            status=status.value,
            price_snapshot= price_snapshot,
            currency_snapshot= currency_snapshot,
        )
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return to_domain(obj)

    async def list_by_client(self, client_id: int) -> list[Subscription]:
        stmt = select(SubscriptionORM).where(
            SubscriptionORM.client_id == client_id,
            SubscriptionORM.is_deleted == False,  # noqa: E712
        ).order_by(SubscriptionORM.id.desc())

        res = await self.db.execute(stmt)
        return [to_domain(x) for x in res.scalars().all()]

    async def get_by_id(self, sub_id: int) -> Subscription | None:
        stmt = select(SubscriptionORM).where(
            SubscriptionORM.id == sub_id,
            SubscriptionORM.is_deleted == False,  # noqa: E712
        )
        res = await self.db.execute(stmt)
        obj = res.scalar_one_or_none()
        return to_domain(obj) if obj else None

    async def update_field(
        self,
        sub_id: int,
        *,
        status: SubscriptionStatus | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> Subscription | None:
        stmt = select(SubscriptionORM).where(
            SubscriptionORM.id == sub_id,
            SubscriptionORM.is_deleted == False,  # noqa: E712
        )
        res = await self.db.execute(stmt)
        obj = res.scalar_one_or_none()
        if not obj:
            return None

        if status is not None:
            obj.status = status.value
        if start_date is not None:
            obj.start_date = start_date
        if end_date is not None:
            obj.end_date = end_date

        await self.db.commit()
        await self.db.refresh(obj)
        return to_domain(obj)

    async def delete(self, sub_id: int) -> bool:
        stmt = select(SubscriptionORM).where(
            SubscriptionORM.id == sub_id,
            SubscriptionORM.is_deleted == False,  # noqa: E712
        )
        res = await self.db.execute(stmt)
        obj = res.scalar_one_or_none()
        if not obj:
            return False

        obj.is_deleted = True
        await self.db.commit()
        return True