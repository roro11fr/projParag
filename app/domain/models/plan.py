from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Plan:
    id: Optional[int]
    name: str
    price: Decimal
    currency: str
    billing_period: str  # monthly / yearly
    is_active: bool
    created_at: datetime | None = None