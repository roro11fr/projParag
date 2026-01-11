from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal
from enum import Enum


class SubscriptionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELED = "CANCELED"

@dataclass(frozen=True)
class Subscription:
    id: int
    client_id: int
    status: SubscriptionStatus
    start_date: date
    end_date: date
    created_at: datetime
    updated_at: datetime