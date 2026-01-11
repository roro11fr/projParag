from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Plan:
    id: int
    name: str
    price: Decimal
    currency: str
    billing_period: str  # monthly / yearly
    is_active: bool