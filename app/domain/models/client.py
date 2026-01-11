from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Client:
    id: int
    company_id: int

    name: str
    fiscal_code: str
    email: str | None
    phone: str | None
    address: str | None

    is_vat_payer: bool
    contact_person: str | None

    is_deleted: bool
    created_at: datetime | None
    updated_at: datetime | None