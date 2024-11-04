from sqlalchemy import Column, Uuid, String, Integer, DateTime, Boolean
from datetime import datetime
import hashlib

from src.models.database import Base

class User(Base):
    __tablename__="User"

    user_id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    _password_hash = Column(String, nullable=False)
    _created_at = Column(DateTime, nullable=False)
    _last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.set_password(password)
        self._created_at = datetime.now()
