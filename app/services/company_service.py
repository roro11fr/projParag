from app.domain.models.company import Company
from app.domain.schemas.company_schema import CompanyCreate, CompanyUpdate
from app.domain.exceptions import CompanyNotFound, CompanyCuiAlreadyExists
from app.infrastructure.repositories.company_repository import CompanyRepository


class CompanyService:
    def __init__(self, repo: CompanyRepository):
        self.repo = repo

    async def list_companies(self) -> list[Company]:
        return await self.repo.get_all()

    async def get_company(self, company_id: int) -> Company:
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise CompanyNotFound()
        return company

    async def create_company(self, payload: CompanyCreate) -> Company:
        existing = await self.repo.get_by_cui(payload.cui)
        if existing:
            raise CompanyCuiAlreadyExists()

        return await self.repo.create(
            name=payload.name,
            cui=payload.cui,
            address=payload.address,
        )

    async def update_company(self, company_id: int, payload: CompanyUpdate) -> Company:
        _ = await self.get_company(company_id)

        updated = await self.repo.update(
            company_id=company_id,
            name=payload.name,
            address=payload.address,
        )
        if not updated:
            raise CompanyNotFound()

        return updated