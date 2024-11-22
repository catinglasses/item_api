from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import UserCreate, UserLogin, UserOut
from src.services.user_service import UserService
from src.services.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from src.models.users import User
from src.models.database import get_db
from src.repositories.user_repository import UserRepository

router = APIRouter()

async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: UserRepository = Depends(get_user_repository)
):
    """Endpoint to log in users"""
    user_service = UserService(user_repository)

    user_login = UserLogin(username=form_data.username, password=form_data.password)
    user = user_service.authenticate_user(user_login=user_login)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/user/create/", response_model=User)
async def register(

):