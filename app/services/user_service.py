from app.domain.models.user import User
from app.domain.schemas.user_schema import UserCreate, UserUpdate
from app.domain.exceptions import (
    UserNotFound,
    EmailAlreadyExists,
    UsernameAlreadyExistsInCompany,
)
from app.domain.security.password_hasher import hash_password
from app.domain.repositories.user_repo import UserRepo


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    async def create_user(self, payload: UserCreate) -> User:
        email_str = str(payload.email)

        if await self.repo.get_by_email(email_str):
            raise EmailAlreadyExists()

        if await self.repo.exists_username_in_company(payload.company_id, payload.username):
            raise UsernameAlreadyExistsInCompany()

        password_hash = hash_password(payload.password)

        return await self.repo.create(
            company_id=payload.company_id,
            username=payload.username,
            email=email_str,
            password_hash=password_hash,
            role=payload.role,
        )

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        return user

    async def list_users(self, company_id: int) -> list[User]:
        return await self.repo.list_by_company(company_id)

    async def update_user(self, user_id: int, payload: UserUpdate) -> User:
        current = await self.repo.get_by_id(user_id)
        if not current:
            raise UserNotFound

        if payload.email is not None:
            email_str = str(payload.email)
            existing = await self.repo.get_by_email(email_str)
            if existing and existing.id != user_id:
                raise EmailAlreadyExists

        if payload.username is not None:
            existing_u = await self.repo.get_by_username_in_company(current.company_id, payload.username)
            if existing_u and existing_u.id != user_id:
                raise UsernameAlreadyExistsInCompany

        password_hash = None
        if payload.password is not None:
            password_hash = hash_password(payload.password)

        updated = await self.repo.update_partial(
            user_id,
            username=payload.username,
            email=str(payload.email) if payload.email is not None else None,
            role=payload.role,
            password_hash=password_hash,
        )

        if not updated:
            raise UserNotFound

        return updated

    async def delete_user(self, user_id: int) -> None:
        deleted = await self.repo.delete(user_id)
        if not deleted:
            raise UserNotFound()