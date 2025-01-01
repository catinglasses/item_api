from uuid import UUID
from datetime import datetime
from sqlalchemy.sql import func
from typing import Optional, Set
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.items import Item
from src.models.database import Base

class User(Base):
    __tablename__="users"

    user_id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    _password_hash: Mapped[str] = mapped_column(nullable=False)
    _created_at: Mapped[datetime] = mapped_column(nullable=False)
    _last_login: Mapped[datetime] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    items: Mapped[Set["Item"]] = relationship(back_populates="creator")
