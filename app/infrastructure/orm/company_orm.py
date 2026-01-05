from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.infrastructure.db.base import Base


class CompanyORM(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    cui = Column(String(32), unique=True, nullable=False)
    address = Column(String(300), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
