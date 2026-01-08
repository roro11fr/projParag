from app.domain.models.company import Company
from app.domain.schemas.company_schema import CompanyCreate
from app.infrastructure.repositories.company_repository import CompanyRepository


class CompanyService:
    def __init__(self, repo: CompanyRepository):
        self.repo = repo

    async def create_company(self, payload: CompanyCreate) -> Company:
        existing = await self.repo.get_by_cui(payload.cui)
        if existing:
            raise ValueError("CUI already exists")

        return await self.repo.create(
            name=payload.name,
            cui=payload.cui,
            address=payload.address,
        )

    async def get_company(self, company_id: int) -> Company | None:
        return await self.repo.get_by_id(company_id)