import hashlib
from datetime import datetime

from src.models.users import User
from src.repositories.user_repository import UserRepository
from src.schemas.users import UserCreate, UserLogin

class UserService:
    '''User management class. User-related operations like create, most getters/setters go here'''
    def __init__(self, user_repository: UserRepository, password_manager: PasswordManager):
        self.user_repository = user_repository
        self.password_manager = password_manager

    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new User via user_repository"""
        new_user = User(
            username=user_create.username,
            email=user_create.email,
            _password_hash=self.password_manager.set_password(user_create.password),
            _created_at=datetime.now(),
        )
        return await self.user_repository.create_user(new_user)

    async def get_created_at(self, user: User) -> datetime:
        """Return user creation timestamp"""
        return user._created_at

    async def get_last_login(self, user: User) -> datetime:
        """Return last login timestamp"""
        return user._last_login

    async def update_last_login(self, user: User) -> None:
        """Update last login timestamp"""
        user._last_login = datetime.now()
        await self.user_repository.update_user(user)
