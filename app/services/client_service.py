import logging
from app.domain.exceptions import ClientNotFound
from app.domain.models.client import Client
from app.domain.repositories.client_repo import ClientRepo
from app.domain.schemas.client_schema import ClientCreate, ClientUpdate

logger = logging.getLogger(__name__)


class ClientService:
    def __init__(self, repo: ClientRepo):
        self.repo = repo

    async def create_client(self, data: ClientCreate) -> Client:
        logger.info(f"client.create | company_id={data.company_id} fiscal_code={data.fiscal_code}")

        email_str = str(data.email) if data.email is not None else None

        client = await self.repo.create(
            company_id=data.company_id,
            name=data.name,
            fiscal_code=data.fiscal_code,
            email=email_str,
            phone=data.phone,
            address=data.address,
            is_vat_payer=data.is_vat_payer,
            contact_person=data.contact_person,
        )

        logger.info(f"client.created | id={client.id}")
        return client

    async def get_client(self, client_id: int) -> Client:
        logger.info(f"client.get | id={client_id}")

        client = await self.repo.get_by_id(client_id)
        if not client:
            logger.warning(f"client.not_found | id={client_id}")
            raise ClientNotFound()

        return client

    async def list_clients(self, company_id: int) -> list[Client]:
        logger.info(f"client.list | company_id={company_id}")
        return await self.repo.list_by_company(company_id)

    async def update_client(self, client_id: int, data: ClientUpdate) -> Client:
        logger.info(f"client.update_partial | id={client_id}")

        updated = await self.repo.update_partial(client_id, data)
        if not updated:
            logger.warning(f"client.not_found | id={client_id}")
            raise ClientNotFound()

        logger.info(f"client.updated | id={client_id}")
        return updated

    async def delete_client(self, client_id: int) -> None:
        logger.info(f"client.soft_delete | id={client_id}")

        ok = await self.repo.soft_delete(client_id)
        if not ok:
            logger.warning(f"client.not_found | id={client_id}")
            raise ClientNotFound()

        logger.info(f"client.deleted | id={client_id}")