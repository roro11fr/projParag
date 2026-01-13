from __future__ import annotations
from typing import Protocol

from app.domain.models.user import User


class UserRepo(Protocol):
    async def get_by_id(self, user_id: int) -> User | None: ...
    async def get_by_email(self, email: str) -> User | None: ...
    async def exists_username_in_company(self, company_id: int, username: str) -> bool: ...

    async def create(
        self,
        *,
        company_id: int,
        username: str,
        email: str,
        password_hash: str,
        role: str,
    ) -> User: ...

    async def list_by_company(self, company_id: int) -> list[User]: ...

    async def get_by_username_in_company(self, company_id: int, username: str) -> User | None: ...

    async def update_partial(
        self,
        user_id: int,
        *,
        username: str | None = None,
        email: str | None = None,
        role: str | None = None,
        password_hash: str | None = None,
    ) -> User | None: ...

    async def delete(self, user_id: int) -> bool: ...