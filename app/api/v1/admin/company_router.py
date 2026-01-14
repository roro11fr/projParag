from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.company_repository import CompanyRepository
from app.services.company_service import CompanyService

from app.domain.models.company import Company
from app.domain.schemas.company_schema import CompanyCreate, CompanyUpdate, CompanyRead

router = APIRouter(
    prefix="/admin/companies",
    tags=["admin-companies"],
)

def get_company_service(db: AsyncSession = Depends(get_db)) -> CompanyService:
    repository = CompanyRepository(db)
    return CompanyService(repository)

def to_company_read(company: Company) -> CompanyRead:
    return CompanyRead(
        id=company.id,
        name=company.name,
        cui=company.cui,
    )

@router.get("/", response_model=list[CompanyRead])
async def list_companies(company_service: CompanyService = Depends(get_company_service)):
    companies = await company_service.list_companies()
    return [to_company_read(company) for company in companies]

@router.get("/{company_id}", response_model=CompanyRead)
async def get_company(company_id: int, company_service: CompanyService = Depends(get_company_service)):
    company = await company_service.get_company(company_id)
    return to_company_read(company)

@router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(payload: CompanyCreate, company_service: CompanyService = Depends(get_company_service)):
    company = await company_service.create_company(payload)
    return to_company_read(company)

@router.put("/{company_id}", response_model=CompanyRead)
async def update_company(company_id: int, payload: CompanyUpdate, company_service: CompanyService = Depends(get_company_service)):
    company = await company_service.update_company(company_id, payload)
    return to_company_read(company)

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, company_service: CompanyService = Depends(get_company_service)):
    await company_service.delete_company(company_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{company_id}", response_model=CompanyRead)
async def patch_company(company_id: int, data: CompanyUpdate, service: CompanyService = Depends(get_company_service)):
    company = await service.update_company(company_id, data)
    return to_company_read(company)