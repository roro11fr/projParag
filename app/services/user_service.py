import logging

from app.domain.models.user import User
from app.domain.schemas.user_schema import UserCreate, UserUpdate
from app.domain.exceptions import (
    UserNotFound,
    EmailAlreadyExists,
    UsernameAlreadyExistsInCompany,
)
from app.domain.security.password_hasher import hash_password
from app.domain.repositories.user_repo import UserRepo

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    async def create_user(self, payload: UserCreate) -> User:
        email_str = str(payload.email)
        logger.info(f"user.create | company_id={payload.company_id} username={payload.username} email={email_str}")

        if await self.repo.get_by_email(email_str):
            logger.warning(f"user.create conflict email | email={email_str}")
            raise EmailAlreadyExists()

        if await self.repo.exists_username_in_company(payload.company_id, payload.username):
            logger.warning(f"user.create conflict username | company_id={payload.company_id} username={payload.username}")
            raise UsernameAlreadyExistsInCompany()

        password_hash = hash_password(payload.password)

        created = await self.repo.create(
            company_id=payload.company_id,
            username=payload.username,
            email=email_str,
            password_hash=password_hash,
            role=payload.role,
        )

        logger.info(f"user.created | id={created.id} company_id={created.company_id}")
        return created

    async def get_user(self, user_id: int) -> User:
        logger.info(f"user.get | id={user_id}")

        user = await self.repo.get_by_id(user_id)
        if not user:
            logger.warning(f"user.not_found | id={user_id}")
            raise UserNotFound()

        return user

    async def list_users(self, company_id: int) -> list[User]:
        logger.info(f"user.list | company_id={company_id}")
        return await self.repo.list_by_company(company_id)

    async def update_user(self, user_id: int, payload: UserUpdate) -> User:
        logger.info(f"user.update_partial | id={user_id}")

        current = await self.repo.get_by_id(user_id)
        if not current:
            logger.warning(f"user.not_found | id={user_id}")
            raise UserNotFound()

        if payload.email is not None:
            email_str = str(payload.email)
            existing = await self.repo.get_by_email(email_str)
            if existing and existing.id != user_id:
                logger.warning(f"user.update conflict email | id={user_id} email={email_str}")
                raise EmailAlreadyExists()

        if payload.username is not None:
            existing_u = await self.repo.get_by_username_in_company(current.company_id, payload.username)
            if existing_u and existing_u.id != user_id:
                logger.warning(
                    f"user.update conflict username | id={user_id} company_id={current.company_id} username={payload.username}"
                )
                raise UsernameAlreadyExistsInCompany()

        password_hash = hash_password(payload.password) if payload.password is not None else None

        updated = await self.repo.update_partial(
            user_id,
            username=payload.username,
            email=str(payload.email) if payload.email is not None else None,
            role=payload.role,
            password_hash=password_hash,
        )

        if not updated:
            logger.warning(f"user.not_found | id={user_id}")
            raise UserNotFound()

        logger.info(f"user.updated | id={user_id}")
        return updated

    async def delete_user(self, user_id: int) -> None:
        logger.info(f"user.delete | id={user_id}")

        deleted = await self.repo.delete(user_id)
        if not deleted:
            logger.warning(f"user.not_found | id={user_id}")
            raise UserNotFound()

        logger.info(f"user.deleted | id={user_id}")