from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
import status

from src.models.users import User
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from src.services.auth_service import TokenService, PasswordManager, UserAuthenticationManager
from src.services.auth_service import ACCESS_TOKEN_EXPIRE_MINUTES
from src.schemas.users import UserCreate, UserLogin, UserOut
from src.models.database import get_db

router = APIRouter()

async def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> UserRepository:
    """Create UserRepository instance, dependency inject async db session"""
    return UserRepository(db)

async def get_password_manager(
    user_repository: UserRepository = Depends(get_user_repository)
) -> PasswordManager:
    """Create PasswordManager instance, dependency inject UserRepository"""
    return PasswordManager(user_repository)

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

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_manager: UserAuthenticationManager = Depends(get_authentication_manager)
):
    """Endpoint to log in users"""
    user_login = UserLogin(username=form_data.username, password=form_data.password)

    user = await auth_manager.authenticate_user(user_login=user_login)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_manager.token_service.create_access_token(
        data={"sub": user.username}, expires_detla=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
