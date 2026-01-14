from fastapi import APIRouter, Depends, Query, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.user_repository import UserRepository
from app.services.user_service import UserService

from app.domain.models.user import User
from app.domain.schemas.user_schema import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/admin/users", tags=["admin-users"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


def to_user_read(user: User) -> UserRead:
    return UserRead(
        id=user.id,
        company_id=user.company_id,
        username=user.username,
        email=str(user.email),   # <- vezi mai jos (EmailStr)
        role=user.role,          # <- vezi mai jos (Literal)
        created_at=user.created_at,
    )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user(user_id)
    return to_user_read(user)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, user_service: UserService = Depends(get_user_service)):
    user = await user_service.create_user(payload)
    return to_user_read(user)


@router.get("/", response_model=list[UserRead])
async def list_users(
    company_id: int = Query(..., ge=1),
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.list_users(company_id)
    return [to_user_read(u) for u in users]


@router.patch("/{user_id}", response_model=UserRead)
async def update_user_patch(user_id: int, payload: UserUpdate, user_service: UserService = Depends(get_user_service)):
    user = await user_service.update_user(user_id, payload)
    return to_user_read(user)


@router.put("/{user_id}", response_model=UserRead)
async def update_user_put(user_id: int, payload: UserUpdate, user_service: UserService = Depends(get_user_service)):
    user = await user_service.update_user(user_id, payload)
    return to_user_read(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    await user_service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)