from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base
class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    reference: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    amount: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(3))
    status: Mapped[str] = mapped_column(String(50), index=True)
    processor: Mapped[str] = mapped_column(String(50))
    processor_transaction_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    payment_method_id: Mapped[str] = mapped_column(String(255))
    card_brand: Mapped[str | None] = mapped_column(String(32), nullable=True)
    card_last_four: Mapped[str | None] = mapped_column(String(4), nullable=True)
    failure_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    failure_message_safe: Mapped[str | None] = mapped_column(Text, nullable=True)
    requires_action: Mapped[bool] = mapped_column(Boolean, default=False)
    next_action_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
