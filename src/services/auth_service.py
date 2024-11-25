import hashlib
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt

from src.models.users import User
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService

SECRET_KEY = "b8a7aaf88a2cb2af28f593fea74eb295"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_access_token(self, data: dict, expires_detla: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_detla:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return credentials_exception
            user = await self.user_repository.get_user_by_username(username)
            if user is None:
                return credentials_exception
            return user

        except JWTError:
            raise credentials_exception

class PasswordManager:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def set_password(self, password: str) -> str:
        """Set password after hashing it"""
        return self.hash_password(password)

    @staticmethod
    def hash_password(self, password: str) -> str:
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()

    async def check_password(self, password: str, user: User) -> bool:
        """Check if provided password matches the hash"""
        return self.hash_password(password) == user._password_hash

class UserAuthenticationManager(TokenService, PasswordManager):
    """Handles user authentication and token generation."""
    def __init__(self, token_service: TokenService, password_manager: PasswordManager):
        self.token_service = token_service
        self.password_manager = password_manager

    async def authenticate_user(self, user_login: UserLogin) -> User | None:
        """Authenticate a user using their username and password."""
        user = await self.user_repository.get_user_by_username(user_login.username)
        if user and await self.password_manager.check_password(user_login.password, user):
            return user
        return None

    def generate_token(self) -> str:
        """Generate a token for the authenticated user."""
        return self.token_service.create_access_token(data={"sub": user.username})
