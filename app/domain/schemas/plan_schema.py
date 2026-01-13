from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, ConfigDict

Currency = Literal["EUR", "USD", "GBP"]
BillingPeriod = Literal["monthly", "yearly"]


class PlanBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    billing_period: BillingPeriod
    is_active: bool = True
    currency: Currency


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    billing_period: Optional[BillingPeriod] = None
    is_active: Optional[bool] = None
    currency: Optional[str] = Field(None, min_length=3, max_length=3)

class PlanRead(PlanBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)