import hashlib
from datetime import datetime
from sqlalchemy.orm import Session

from src.models.users import User
from src.repositories.user_repository import UserRepository
from src.schemas.users import UserCreate, UserLogin

class UserService:
    '''User management class. User-related operations like create, authenticate and others go here'''
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_create: UserCreate) -> User:
        """Create a new User via user_repository"""
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

    def set_password(self, password: str) -> str:
        """Set password after hashing it"""
        self._password_hash = self.hash_password(password)

    @staticmethod
    def hash_password(self, password: str) -> str:
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str, user: User) -> bool:
        """Check if provided password matches the hash"""
        return self.hash_password(password) == user.get_password_hash()

    def authenticate_user(self, user_login: UserLogin) -> User | None:
        """Authenticate a user using their username and password"""
        user = self.user_repository.get_user_by_username(user_login.username)
        if user and self.check_password:
            return user
        return None

    def get_created_at(self, user: User):
        """Return user creation timestamp"""
        return user._created_at

    def get_last_login(self, user: User):
        """Return last login timestamp"""
        return user._last_login

    def update_last_login(self, user: User):
        """Update last login timestamp"""
        user._last_login = datetime.now()
        self.user_repository.update_user(user)
