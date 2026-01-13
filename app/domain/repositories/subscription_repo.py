from __future__ import annotations

from typing import Protocol
from datetime import date
from decimal import Decimal

from app.domain.models.subscription import Subscription, SubscriptionStatus


class SubscriptionRepo(Protocol):
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
    ) -> Subscription: ...

    async def list_by_client(self, client_id: int) -> list[Subscription]: ...

    async def get_by_id(self, sub_id: int) -> Subscription | None: ...

    async def update_field(
        self,
        sub_id: int,
        *,
        status: SubscriptionStatus | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> Subscription | None: ...

    async def delete(self, sub_id: int) -> bool: ...