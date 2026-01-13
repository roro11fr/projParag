from __future__ import annotations
from typing import Protocol

from app.domain.models.client import Client
from app.domain.schemas.client_schema import ClientUpdate


class ClientRepo(Protocol):
    async def create(
        self,
        *,
        company_id: int,
        name: str,
        fiscal_code: str,
        email: str | None,
        phone: str | None,
        address: str | None,
        is_vat_payer: bool,
        contact_person: str | None,
    ) -> Client: ...

    async def get_by_id(self, client_id: int) -> Client | None: ...
    async def list_by_company(self, company_id: int) -> list[Client]: ...

    async def update_partial(self, client_id: int, data: ClientUpdate) -> Client | None: ...

    async def soft_delete(self, client_id: int) -> bool: ...