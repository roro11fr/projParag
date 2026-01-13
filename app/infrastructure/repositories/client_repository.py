from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.client import Client
from app.domain.repositories.client_repo import ClientRepo
from app.domain.schemas.client_schema import ClientUpdate
from app.infrastructure.mappers.client_mapper import to_domain
from app.infrastructure.orm.client_orm import ClientORM


class ClientRepository(ClientRepo):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, client_id: int) -> Client | None:
        stmt = select(ClientORM).where(
            (ClientORM.id == client_id) &
            (ClientORM.is_deleted.is_(False))
        )
        res = await self.db.execute(stmt)
        row = res.scalar_one_or_none()
        return to_domain(row) if row else None

    async def list_by_company(self, company_id: int) -> list[Client]:
        stmt = select(ClientORM).where(
            (ClientORM.company_id == company_id) &
            (ClientORM.is_deleted.is_(False))
        )
        res = await self.db.execute(stmt)
        rows = res.scalars().all()
        return [to_domain(r) for r in rows]

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
    ) -> Client:
        obj = ClientORM(
            company_id=company_id,
            name=name,
            fiscal_code=fiscal_code,
            email=email,
            phone=phone,
            address=address,
            is_vat_payer=is_vat_payer,
            contact_person=contact_person,
        )
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return to_domain(obj)

    async def save(self, client: ClientORM) -> Client:
        self.db.add(client)
        await self.db.commit()
        await self.db.refresh(client)
        return to_domain(client)

    async def update_partial(self, client_id: int, data: ClientUpdate) -> Client | None:
        res = await self.db.execute(
            select(ClientORM).where(
                (ClientORM.id == client_id) & (ClientORM.is_deleted.is_(False))
            )
        )
        row = res.scalar_one_or_none()
        if not row:
            return None

        row.update_from_dto(data)
        await self.db.commit()
        await self.db.refresh(row)
        return to_domain(row)

    async def soft_delete(self, client_id: int) -> bool:
        res = await self.db.execute(
            select(ClientORM).where(
                (ClientORM.id == client_id) & (ClientORM.is_deleted.is_(False))
            )
        )
        row = res.scalar_one_or_none()
        if not row:
            return False

        row.soft_delete()
        await self.db.commit()
        return True