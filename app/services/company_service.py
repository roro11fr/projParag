import logging

from app.domain.models.company import Company
from app.domain.repositories.company_repo import CompanyRepo
from app.domain.schemas.company_schema import CompanyCreate, CompanyUpdate
from app.domain.exceptions import CompanyNotFound, CompanyCuiAlreadyExists

logger = logging.getLogger(__name__)

class CompanyService:
    def __init__(self, repo: CompanyRepo):
        self.repo = repo

    async def list_companies(self) -> list[Company]:
        logger.info("company.list")
        return await self.repo.get_all()

    async def get_company(self, company_id: int) -> Company:
        logger.info(f"company.get | id={company_id}")
        company = await self.repo.get_by_id(company_id)
        if not company:
            logger.warning(f"company.not_found | id={company_id}")
            raise CompanyNotFound()
        return company

    async def create_company(self, payload: CompanyCreate) -> Company:
        logger.info(f"company.create | name={payload.name} cui={payload.cui}")
        existing = await self.repo.get_by_cui(payload.cui)
        if existing:
            logger.warning(f"company.create conflict | cui={payload.cui}")
            raise CompanyCuiAlreadyExists()

        return await self.repo.create(
            name=payload.name,
            cui=payload.cui,
            address=payload.address,
        )

    async def update_company(self, company_id: int, payload: CompanyUpdate) -> Company:
        logger.info(f"company.update | id={company_id}")
        _ = await self.get_company(company_id)

        updated = await self.repo.update(
            company_id=company_id,
            name=payload.name,
            address=payload.address,
        )
        if not updated:
            logger.warning(f"company.not_found | id={company_id}")
            raise CompanyNotFound(company_id)

        return updated

    async def delete_company(self, company_id: int) -> None:
        logger.info(f"company.delete | id={company_id}")
        deleted = await self.repo.delete(company_id)
        if not deleted:
            raise CompanyNotFound()