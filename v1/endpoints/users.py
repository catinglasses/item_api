from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
import status

from src.models.users import User
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository
from src.schemas.users import UserCreate, UserLogin, UserOut
from src.services.auth_service import ACCESS_TOKEN_EXPIRE_MINUTES
from src.services.auth_service import TokenService, PasswordManager, UserAuthenticationManager
from src.dependencies import get_user_service, get_password_manager, get_token_service, get_authentication_manager, get_current_user

router = APIRouter()

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_manager: UserAuthenticationManager = Depends(get_authentication_manager),
    user_service: UserService = Depends(get_user_service),
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

    await user_service.update_last_login(user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_manager.token_service.create_access_token(
        data={"sub": user.username}, expires_detla=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/create/", response_model=UserOut)
async def register(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Endpoint to register a new user"""
    return await user_service.create_user(user_create)

@router.put("/users/{user_id}/update-password/")
async def update_user_password(
    user_id: UUID,
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Endpoint to update User's password"""
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this password")
    return await user_service.update_password(user_id, current_password, new_password)

@router.get("/users/")
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    """Endpoint to retrieve all User objects"""
    return await user_service.get_all_users()

@router.get("/users/{user_id}/", response_model=UserOut)
async def get_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    """Endpoint to retrieve a specific User by ID"""
    return await user_service.get_user_or_404(user_id)

@router.get("/users/{user_id}/delete/")
async def delete_user(user_id: UUID, user_service: Depends(get_user_service)):
    """Endpoint to delete User after retrieving it by its ID"""
    return await user_service.delete_user(user_id)
