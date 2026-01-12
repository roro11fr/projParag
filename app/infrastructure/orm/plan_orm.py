from sqlalchemy import Boolean, Column, Integer, String, Numeric
from app.infrastructure.db.base import Base


class PlanORM(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    billing_period = Column(String(20), nullable=False)  # monthly/yearly
    is_active = Column(Boolean, default=True, nullable=False)