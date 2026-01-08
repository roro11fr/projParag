from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.company_schema import CompanyCreate, CompanyRead
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.company_repository import CompanyRepository
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


def get_company_service(db: AsyncSession = Depends(get_db)) -> CompanyService:
    return CompanyService(CompanyRepository(db))


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(payload: CompanyCreate, service: CompanyService = Depends(get_company_service)):
    try:
        company = await service.create_company(payload)
        return CompanyRead.model_validate(company)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{company_id}", response_model=CompanyRead)
async def get_company(company_id: int, service: CompanyService = Depends(get_company_service)):
    company = await service.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return CompanyRead.model_validate(company)