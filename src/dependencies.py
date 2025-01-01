from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.models.database import get_db
from src.services.user_service import UserService
from src.services.item_service import ItemService
from src.services.auth_service import oauth2_scheme
from src.repositories.user_repository import UserRepository
from src.repositories.item_repository import ItemRepository
from src.services.auth_service import TokenService, PasswordManager, UserAuthenticationManager

async def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> UserRepository:
    """Create UserRepository instance, dependency inject async db session"""
    return UserRepository(db)

async def get_item_repository(
    db: AsyncSession = Depends(get_db)
) -> ItemRepository:
    """Create ItemRepository instance, dependency inject async db session"""
    return ItemRepository(db)

async def get_password_manager(
    user_repository: UserRepository = Depends(get_user_repository)
) -> PasswordManager:
    """Create PasswordManager instance, dependency inject UserRepository"""
    return PasswordManager(user_repository)

async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    password_manager: PasswordManager = Depends(get_password_manager)
) -> UserService:
    """Create UserService instance, DI UserRepository, PasswordManager"""
    return UserService(user_repository, password_manager)

async def get_token_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> TokenService:
    """Create TokenService instance, dependency inject UserRepository"""
    return TokenService(user_repository)

async def get_authentication_manager(
    token_service: TokenService = Depends(get_token_service),
    password_manager: PasswordManager = Depends(get_password_manager)
) -> UserAuthenticationManager:
    """Create UserAuthenticationManager, DI TokenService & PasswordManager"""
    return UserAuthenticationManager(token_service, password_manager)

async def get_item_service(
    item_repository: ItemRepository = Depends(get_item_repository)
) -> ItemService:
    """Create ItemService instance, DI ItemRepository and UserAuthenticationManager"""
    return ItemService(item_repository)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_service: TokenService = Depends(get_token_service)
) -> User:
    return await token_service.get_current_user(token)
