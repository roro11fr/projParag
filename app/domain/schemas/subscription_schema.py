from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.domain.models.subscription import SubscriptionStatus


class SubscriptionCreate(BaseModel):
    start_date: date
    end_date: date
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE


class SubscriptionPatch(BaseModel):
    status: Optional[SubscriptionStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class SubscriptionRead(BaseModel):
    id: int
    client_id: int
    status: SubscriptionStatus
    start_date: date
    end_date: date
    created_at: datetime
    updated_at: datetime


class RenewRequest(BaseModel):
    months: int = Field(ge=1, le=36)