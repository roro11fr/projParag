from __future__ import annotations

from app.domain.exceptions import ClientNotFound
from app.domain.models.client import Client
from app.domain.schemas.client_schema import ClientCreate, ClientUpdate
from app.infrastructure.orm.client_orm import ClientORM
from app.infrastructure.repositories.client_repository import ClientRepository


class ClientService:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    async def create_client(self, data: ClientCreate) -> Client:
        client_row = ClientORM(**data.model_dump())
        return await self.repo.create(client_row)

    async def list_clients(self, company_id: int) -> list[Client]:
        return await self.repo.list_by_company(company_id)

    async def get_client(self, client_id: int) -> Client:
        client = await self.repo.get_by_id(client_id)
        if not client:
            raise ClientNotFound()
        return client

    async def update_client(self, client_id: int, data: ClientUpdate) -> Client:
        updated = await self.repo.update_partial(client_id, data)
        if not updated:
            raise ClientNotFound()
        return updated

    async def delete_client(self, client_id: int) -> None:
        ok = await self.repo.soft_delete(client_id)
        if not ok:
            raise ClientNotFound()