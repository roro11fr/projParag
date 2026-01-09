from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CompanyCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    cui: str = Field(..., min_length=2, max_length=32)
    address: Optional[str] = Field(None, max_length=300)


class CompanyRead(BaseModel):
    id: int
    name: str
    cui: str

    model_config = ConfigDict(from_attributes=True)

class CompanyUpdate(BaseModel):
    name: str | None = Field(None, max_length=200)
    address: str | None = None