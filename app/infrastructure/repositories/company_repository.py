from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.company import Company
from app.infrastructure.orm.company_orm import CompanyORM


def _to_domain(c: CompanyORM) -> Company:
    return Company(
        id=c.id,
        name=c.name,
        cui=c.cui,
        address=c.address,
        created_at=c.created_at,
    )


class CompanyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, company_id: int) -> Company | None:
        res = await self.db.execute(select(CompanyORM).where(CompanyORM.id == company_id))
        row = res.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def get_by_cui(self, cui: str) -> Company | None:
        res = await self.db.execute(select(CompanyORM).where(CompanyORM.cui == cui))
        row = res.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def create(self, *, name: str, cui: str, address: str | None) -> Company:
        c = CompanyORM(name=name, cui=cui, address=address)
        self.db.add(c)
        await self.db.commit()
        await self.db.refresh(c)
        return _to_domain(c)