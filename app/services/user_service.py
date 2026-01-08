import hashlib

from app.domain.models.user import User
from app.domain.schemas.user_schema import UserCreate
from app.infrastructure.repositories.user_repository import UserRepository


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, payload: UserCreate) -> User:
        email_str = str(payload.email)
        existing_email = await self.repo.get_by_email(email_str)

        if existing_email:
            raise ValueError("Email already exists")

        if await self.repo.exists_username_in_company(payload.company_id, payload.username):
            raise ValueError("Username already exists in this company")

        password_hash = _hash_password(payload.password)

        return await self.repo.create(
            company_id=payload.company_id,
            username=payload.username,
            email=email_str,
            password_hash=password_hash,
            role=payload.role,
        )

    async def get_user(self, user_id: int) -> User | None:
        return await self.repo.get_by_id(user_id)

    async def list_users(self, company_id: int) -> list[User]:
        return await self.repo.list_by_company(company_id)