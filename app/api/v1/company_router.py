from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.company_repository import CompanyRepository
from app.services.company_service import CompanyService

from app.domain.models.company import Company
from app.domain.schemas.company_schema import (
    CompanyCreate,
    CompanyUpdate,
    CompanyRead,
)
from app.domain.exceptions import (
    CompanyNotFound,
    CompanyCuiAlreadyExists,
)

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)


# ---------- Dependency wiring ----------

def get_company_service(
    db: AsyncSession = Depends(get_db),
) -> CompanyService:
    repository = CompanyRepository(db)
    return CompanyService(repository)


# ---------- DTO mapper ----------

def to_company_read(company: Company) -> CompanyRead:
    """
    Maps domain Company → CompanyRead DTO.
    Explicit mapping = clear + safe + SOLID.
    """
    return CompanyRead(
        id=company.id,
        name=company.name,
        cui=company.cui,
    )


# ---------- Endpoints ----------

@router.get(
    "/",
    response_model=list[CompanyRead],
)
async def list_companies(
    company_service: CompanyService = Depends(get_company_service),
):
    companies = await company_service.list_companies()
    return [to_company_read(company) for company in companies]


@router.get(
    "/{company_id}",
    response_model=CompanyRead,
)
async def get_company(
    company_id: int,
    company_service: CompanyService = Depends(get_company_service),
):
    try:
        company = await company_service.get_company(company_id)
        return to_company_read(company)
    except CompanyNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )


@router.post(
    "/",
    response_model=CompanyRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_company(
    payload: CompanyCreate,
    company_service: CompanyService = Depends(get_company_service),
):
    try:
        company = await company_service.create_company(payload)
        return to_company_read(company)
    except CompanyCuiAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company with this CUI already exists",
        )


@router.put(
    "/{company_id}",
    response_model=CompanyRead,
)
async def update_company(
    company_id: int,
    payload: CompanyUpdate,
    company_service: CompanyService = Depends(get_company_service),
):
    try:
        company = await company_service.update_company(company_id, payload)
        return to_company_read(company)
    except CompanyNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )