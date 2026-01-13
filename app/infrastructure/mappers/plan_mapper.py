from app.domain.models.plan import Plan
from app.infrastructure.orm.plan_orm import PlanORM


def to_domain(plan_orm: PlanORM) -> Plan:
    return Plan(
        id=plan_orm.id,
        name=plan_orm.name,
        price=plan_orm.price,
        currency=plan_orm.currency,
        billing_period=plan_orm.billing_period,
        is_active=plan_orm.is_active,
        created_at=plan_orm.created_at
    )