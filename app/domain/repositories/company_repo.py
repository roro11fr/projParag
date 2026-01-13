from __future__ import annotations

from typing import Protocol

from app.domain.models.company import Company


class CompanyRepo(Protocol):
    # ---------- READ ----------
    async def get_all(self) -> list[Company]: ...
    async def get_by_id(self, company_id: int) -> Company | None: ...
    async def get_by_cui(self, cui: str) -> Company | None: ...

    # ---------- WRITE ----------
    async def create(
        self,
        *,
        name: str,
        cui: str,
        address: str | None,
    ) -> Company: ...

    async def update(
        self,
        company_id: int,
        *,
        name: str | None,
        address: str | None,
    ) -> Company | None: ...

    async def delete(self, company_id: int) -> bool: ...