from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class ClientBase(BaseModel):
    name: str
    fiscal_code: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_vat_payer: bool = False
    contact_person: Optional[str] = None


class ClientCreate(ClientBase):
    company_id: int


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_vat_payer: Optional[bool] = None
    contact_person: Optional[str] = None


class ClientRead(ClientBase):
    id: int
    company_id: int

    model_config = ConfigDict(from_attributes=True)
