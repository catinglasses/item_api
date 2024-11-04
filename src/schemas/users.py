from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    user_id: UUID
    username: str
    email: str

    class Config:
        orm_mode = True