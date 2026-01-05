from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.user import User
from app.infrastructure.orm.user_orm import UserORM


def _to_domain(u: UserORM) -> User:
    return User(
        id=u.id,
        company_id=u.company_id,
        username=u.username,
        email=u.email,
        role=u.role,
        created_at=u.created_at,
    )


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        res = await self.db.execute(select(UserORM).where(UserORM.id == user_id))
        row = res.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def get_by_email(self, email: str) -> User | None:
        res = await self.db.execute(select(UserORM).where(UserORM.email == email))
        row = res.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def exists_username_in_company(self, company_id: int, username: str) -> bool:
        stmt = select(UserORM.id).where(
            (UserORM.company_id == company_id) & (UserORM.username == username)
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none() is not None

    async def create(self, *, company_id: int, username: str, email: str, password_hash: str, role: str) -> User:
        u = UserORM(
            company_id=company_id,
            username=username,
            email=email,
            password=password_hash,
            role=role,
        )
        self.db.add(u)
        await self.db.commit()
        await self.db.refresh(u)
        return _to_domain(u)