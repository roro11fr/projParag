from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.domain.models.subscription import SubscriptionStatus


# ---------- CREATE ----------
class SubscriptionCreate(BaseModel):
    plan_id: int
    start_date: date
    end_date: date
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE


# ---------- PATCH (admin / system actions) ----------
class SubscriptionPatch(BaseModel):
    status: Optional[SubscriptionStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


# ---------- READ ----------
class SubscriptionRead(BaseModel):
    id: int
    client_id: int
    plan_id: int
    client_name: str

    status: SubscriptionStatus
    start_date: date
    end_date: Optional[date]

    created_at: datetime
    updated_at: datetime


# ---------- RENEW ----------
class RenewRequest(BaseModel):
    months: int = Field(ge=1, le=36)