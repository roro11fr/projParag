from app.domain.models.user import User
from app.infrastructure.orm import UserORM

def _to_domain(u: UserORM) -> User:
    return User(
        id=u.id,
        company_id=u.company_id,
        username=u.username,
        email=u.email,
        role=u.role,
        created_at=u.created_at,
    )