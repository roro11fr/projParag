from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.user import User
from app.domain.repositories.user_repo import UserRepo
from app.infrastructure.mappers.user_mapper import _to_domain
from app.infrastructure.orm.user_orm import UserORM




class UserRepository(UserRepo):
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

    async def list_by_company(self, company_id: int) -> list[User]:
        stmt = (
            select(UserORM)
            .where(UserORM.company_id == company_id)
            .order_by(UserORM.id.asc())
        )
        res = await self.db.execute(stmt)
        rows = res.scalars().all()
        return [_to_domain(u) for u in rows]

    async def update(
            self,
            user_id: int,
            *,
            username: str | None,
            email: str | None,
            password_hash: str | None,
            role: str | None,
    ):
        res = await self.db.execute(select(UserORM).where(UserORM.id == user_id))
        user_row = res.scalar_one_or_none()
        if not user_row:
            return None

        if username is not None:
            user_row.username = username
        if email is not None:
            user_row.email = email
        if password_hash is not None:
            user_row.password_hash = password_hash
        if role is not None:
            user_row.role = role

        await self.db.commit()
        await self.db.refresh(user_row)
        return _to_domain(user_row)

    async def get_by_username_in_company(self, company_id: int, username: str) -> User | None:
        stmt = select(UserORM).where(
            (UserORM.company_id == company_id) & (UserORM.username == username)
        )
        res = await self.db.execute(stmt)
        row = res.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def update_partial(
            self,
            user_id: int,
            *,
            username: str | None = None,
            email: str | None = None,
            role: str | None = None,
            password_hash: str | None = None,
    ) -> User | None:
        res = await self.db.execute(select(UserORM).where(UserORM.id == user_id))
        u = res.scalar_one_or_none()
        if not u:
            return None

        if username is not None:
            u.username = username
        if email is not None:
            u.email = email
        if role is not None:
            u.role = role
        if password_hash is not None:
            u.password = password_hash

        await self.db.commit()
        await self.db.refresh(u)
        return _to_domain(u)

    async def delete(self, user_id: int) -> bool:
        result = await self.db.execute(
            select(UserORM).where(UserORM.id == user_id)
        )
        user_row = result.scalar_one_or_none()
        if not user_row:
            return False

        await self.db.delete(user_row)
        await self.db.commit()
        return True

