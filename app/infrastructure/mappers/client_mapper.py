from __future__ import annotations

from app.domain.models.client import Client
from app.infrastructure.orm.client_orm import ClientORM


def _to_domain(row: ClientORM) -> Client:
    return Client(
        id=row.id,
        company_id=row.company_id,
        name=row.name,
        fiscal_code=row.fiscal_code,
        email=row.email,
        phone=row.phone,
        address=row.address,
        is_vat_payer=row.is_vat_payer,
        contact_person=row.contact_person,
        is_deleted=row.is_deleted,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )