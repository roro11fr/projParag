from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.user_repository import UserRepository
from app.services.user_service import UserService

from app.domain.models.user import User
from app.domain.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.domain.exceptions import (
    UserNotFound,
    EmailAlreadyExists,
    UsernameAlreadyExistsInCompany,
)

router = APIRouter(prefix="/admin/users", tags=["admin-users"])


# ---------- Dependency wiring ----------

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository)


# ---------- DTO mapper ----------

def to_user_read(user: User) -> UserRead:
    """
    Maps domain User -> UserRead DTO.
    Explicit mapping keeps API stable and avoids leaking internal models.
    """
    return UserRead(
        id=user.id,
        company_id=user.company_id,
        username=user.username,
        email=user.email,
        role=user.role,
        created_at=user.created_at
    )


# ---------- Endpoints ----------

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.get_user(user_id)
        return to_user_read(user)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.create_user(payload)
        return to_user_read(user)
    except EmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )
    except UsernameAlreadyExistsInCompany:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists in this company",
        )


@router.get("/", response_model=list[UserRead])
async def list_users(
    company_id: int = Query(..., ge=1),
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.list_users(company_id)
    return [to_user_read(user) for user in users]

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.update_user(user_id, payload)
        return to_user_read(user)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except EmailAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    except UsernameAlreadyExistsInCompany:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists in this company")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    try:
        await user_service.delete_user(user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    try:
        user = await service.update_user(user_id, data)
        return to_user_read(user)

    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    except EmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )