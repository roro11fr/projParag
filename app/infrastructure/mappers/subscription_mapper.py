from app.domain.models.subscription import Subscription, SubscriptionStatus
from app.infrastructure.orm.subscription_orm import SubscriptionORM


def to_domain(o: SubscriptionORM) -> Subscription:
    return Subscription(
        id=o.id,
        client_id=o.client_id,
        status=SubscriptionStatus(o.status),
        start_date=o.start_date,
        end_date=o.end_date,
        created_at=o.created_at,
        updated_at=o.updated_at,
    )