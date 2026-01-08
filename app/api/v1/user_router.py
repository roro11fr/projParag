from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.user_schema import UserCreate, UserRead
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from fastapi import Query

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        user = await service.create_user(payload)
        return UserRead.model_validate(user)  # from_attributes=True în UserRead
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.get("", response_model=list[UserRead])
async def list_users(
    company_id: int = Query(..., ge=1),
    service: UserService = Depends(get_user_service),
):
    users = await service.list_users(company_id)
    return [UserRead.model_validate(u) for u in users]
