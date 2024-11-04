import hashlib
from datetime import datetime
from sqlalchemy.orm import Session

from src.models.users import User
from src.repositories.user_repository import UserRepository
from src.schemas.users import UserCreate

class UserService:
    def __init__(self, db_session: Session):
        self.user_repository = UserRepository(db_session)

    def create_user(self, user_create: UserCreate) -> User:
        new_user = User(
            username=user_create.username,
            email=user_create.email,
            _password_hash=self.set_password(user_create.password),
            _created_at=datetime.now()
        )
        return self.user_repository.create_user(new_user)

    def get_password_hash(self):
        """Return the hashed password (for internal use)"""
        return self._password_hash

    def set_password(self, password: str):
        """Set password after hashing it"""
        self._password_hash = self.hash_password(password)

    def hash_password(self, password: str) -> str:
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        """Check if provided password matches the hash"""
        return self.hash_password(password) == self._password_hash

    def get_created_at(self):
        return self._created_at

    def get_last_login(self):
        return self._last_login