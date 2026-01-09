from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.models.company import Company
from app.infrastructure.orm.company_orm import CompanyORM
from app.infrastructure.mappers.company_mapper import to_domain

class CompanyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Company]:
        res = await self.db.execute(select(CompanyORM))
        rows = res.scalars().all()
        return [to_domain(r) for r in rows]

    async def get_by_id(self, company_id: int) -> Company | None:
        res = await self.db.execute(
            select(CompanyORM).where(CompanyORM.id == company_id)
        )
        row = res.scalar_one_or_none()
        return to_domain(row) if row else None

    async def get_by_cui(self, cui: str) -> Company | None:
        res = await self.db.execute(
            select(CompanyORM).where(CompanyORM.cui == cui)
        )
        row = res.scalar_one_or_none()
        return to_domain(row) if row else None

    async def create(self, *, name: str, cui: str, address: str | None) -> Company:
        c = CompanyORM(name=name, cui=cui, address=address)
        self.db.add(c)
        await self.db.commit()
        await self.db.refresh(c)
        return to_domain(c)

    async def update(
        self,
        company_id: int,
        *,
        name: str | None,
        address: str | None
    ) -> Company | None:
        # update la nivel ORM, dar return Domain
        res = await self.db.execute(
            select(CompanyORM).where(CompanyORM.id == company_id)
        )
        row = res.scalar_one_or_none()
        if not row:
            return None

        if name is not None:
            row.name = name
        if address is not None:
            row.address = address

        await self.db.commit()
        await self.db.refresh(row)
        return to_domain(row)