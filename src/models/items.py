from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from uuid import UUID
from typing import Optional, Set
from datetime import date, datetime

from src.models.database import Base

class Item(Base):
    __tablename__ = "items"

    item_id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    _created_at: Mapped[date] = mapped_column(nullable=False)
    _last_updated: Mapped[datetime] = mapped_column(nullable=False)
    is_available: Mapped[bool] = mapped_column(default=False)
    amount: Mapped[int] = mapped_column(default=0)
    _created_by: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))
    creator: Mapped["User"] = relationship(back_populates="items")
