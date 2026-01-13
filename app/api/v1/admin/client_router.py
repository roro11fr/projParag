from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.client_repository import ClientRepository
from app.services.client_service import ClientService

from app.domain.models.client import Client
from app.domain.schemas.client_schema import ClientCreate, ClientRead, ClientUpdate
from app.domain.exceptions import ClientNotFound


router = APIRouter(prefix="/admin/clients", tags=["admin-clients"])


def get_client_service(db: AsyncSession = Depends(get_db)) -> ClientService:
    return ClientService(ClientRepository(db))


def to_client_read(c: Client) -> ClientRead:
    return ClientRead(
        id=c.id,
        company_id=c.company_id,
        name=c.name,
        fiscal_code=c.fiscal_code,
        email=c.email,
        phone=c.phone,
        address=c.address,
        is_vat_payer=c.is_vat_payer,
        contact_person=c.contact_person,
    )

@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
async def create_client(payload: ClientCreate, svc: ClientService = Depends(get_client_service)):
    client = await svc.create_client(payload)
    return to_client_read(client)


@router.get("", response_model=list[ClientRead])
async def list_clients(company_id: int, svc: ClientService = Depends(get_client_service)):
    clients = await svc.list_clients(company_id)
    return [to_client_read(c) for c in clients]


@router.get("/{client_id}", response_model=ClientRead)
async def get_client(client_id: int, svc: ClientService = Depends(get_client_service)):
    try:
        client = await svc.get_client(client_id)
        return to_client_read(client)
    except ClientNotFound:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Client not found")


@router.put("/{client_id}", response_model=ClientRead)
async def update_client(client_id: int, payload: ClientUpdate, svc: ClientService = Depends(get_client_service)):
    try:
        client = await svc.update_client(client_id, payload)
        return to_client_read(client)
    except ClientNotFound:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Client not found")


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: int, svc: ClientService = Depends(get_client_service)):
    try:
        await svc.delete_client(client_id)
    except ClientNotFound:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Client not found")