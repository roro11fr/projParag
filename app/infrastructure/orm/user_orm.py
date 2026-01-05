from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.infrastructure.db.base import Base
from app.infrastructure.orm.company_orm import CompanyORM


class UserORM(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)

    username = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(String(16), default="contabil", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship(CompanyORM, backref="users")