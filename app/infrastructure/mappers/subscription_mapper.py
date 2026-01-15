from app.infrastructure.orm.subscription_orm import SubscriptionORM
from app.domain.models.subscription import Subscription, SubscriptionStatus

def to_domain(o: SubscriptionORM, client_name: str | None = None) -> Subscription:
    return Subscription(
        id=o.id,
        client_id=o.client_id,
        client_name=client_name,
        status=SubscriptionStatus(o.status),
        start_date=o.start_date,
        end_date=o.end_date,
        created_at=o.created_at,
        updated_at=o.updated_at,
        plan_id=o.plan_id,
        price_snapshot=o.price_snapshot,
        currency_snapshot=o.currency_snapshot,
    )