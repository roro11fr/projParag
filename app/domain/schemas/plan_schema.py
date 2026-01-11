from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class PlanRead(BaseModel):
    id: int
    name: str
    price: Decimal
    currency: str
    billing_period: str

    model_config = ConfigDict(from_attributes=True)
