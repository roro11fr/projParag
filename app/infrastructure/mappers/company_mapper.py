from app.domain.models.company import Company
from app.infrastructure.orm.company_orm import CompanyORM

def to_domain(row: CompanyORM) -> Company:
    return Company(
        id=row.id,
        name=row.name,
        cui=row.cui,
        address=row.address,
        created_at=row.created_at,
    )