from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class SubscriptionORM(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("client.id"), index=True, nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    plan_id: Mapped[int] = mapped_column(ForeignKey("plan.id"), nullable=False)
    price_snapshot = mapped_column(Numeric(10, 2), nullable=False)
    currency_snapshot = mapped_column(String(3), nullable=False)