from pydantic import BaseModel
from uuid import UUID

class User(BaseModel):
    user_id: UUID
    username: str
    email: str
    is_active: bool

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    user_id: UUID
    username: str
    email: str

    class Config:
        from_attributes = True