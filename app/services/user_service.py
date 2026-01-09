from app.domain.models.user import User
from app.domain.schemas.user_schema import UserCreate
from app.domain.exceptions import (
    UserNotFound,
    EmailAlreadyExists,
    UsernameAlreadyExistsInCompany,
)
from app.domain.security.password_hasher import hash_password
from app.infrastructure.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
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