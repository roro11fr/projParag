from __future__ import annotations

from app.domain.exceptions import ClientNotFound
from app.domain.models.client import Client
from app.domain.repositories.client_repo import ClientRepo
from app.domain.schemas.client_schema import ClientCreate, ClientUpdate


class ClientService:
    def __init__(self, repo: ClientRepo):
        self.repo = repo

    async def create_client(self, data: ClientCreate) -> Client:
        """
        Creates a client under a company.
        DTO -> Domain params, then repo.
        """
        # EmailStr -> str | None (normalize)
        email_str = str(data.email) if data.email is not None else None

        return await self.repo.create(
            company_id=data.company_id,
            name=data.name,
            fiscal_code=data.fiscal_code,
            email=email_str,
            phone=data.phone,
            address=data.address,
            is_vat_payer=data.is_vat_payer,
            contact_person=data.contact_person,
        )

    async def get_client(self, client_id: int) -> Client:
        client = await self.repo.get_by_id(client_id)
        if not client:
            raise ClientNotFound()
        return client

    async def list_clients(self, company_id: int) -> list[Client]:
        return await self.repo.list_by_company(company_id)

    async def update_client(self, client_id: int, data: ClientUpdate) -> Client:
        current = await self.repo.get_by_id(client_id)
        if not current:
            raise ClientNotFound()

        # normalize EmailStr -> str | None
        email_str = str(data.email) if data.email is not None else None

        updated = await self.repo.update(
            client_id,
            name=data.name,
            email=email_str if data.email is not None else None,
            phone=data.phone,
            address=data.address,
            is_vat_payer=data.is_vat_payer,
            contact_person=data.contact_person,
        )
        if not updated:
            raise ClientNotFound()
        return updated

    async def delete_client(self, client_id: int) -> None:
        ok = await self.repo.delete(client_id)
        if not ok:
            raise ClientNotFound()
