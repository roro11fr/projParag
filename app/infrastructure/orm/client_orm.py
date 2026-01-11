from __future__ import annotations

from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base


class ClientORM(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False, index=True)

    name = Column(String(200), nullable=False)
    fiscal_code = Column(String(32), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(40), nullable=True)
    address = Column(String(300), nullable=True)

    is_vat_payer = Column(Boolean, default=False, nullable=False)
    contact_person = Column(String(120), nullable=True)

    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    company = relationship("CompanyORM", back_populates="clients")

    __table_args__ = (
        Index("ix_client_company_name", "company_id", "name"),
    )

    def soft_delete(self) -> None:
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def update_from_dto(self, dto) -> None:
        # dto = Pydantic schema (ClientUpdate)
        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(self, field, value)