from uuid import UUID
from fastapi import Query
from pydantic import BaseModel
from datetime import date, datetime

class ItemSchema(BaseModel):
    item_id: UUID
    name: str
    description: str | None = None
    is_available: bool | None = None
    amount: int = Query(None, ge=0, le=9999)
    _created_by: UUID

class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    amount: int | None = 0
    is_available: bool | None = False

class ItemPatchSchema(BaseModel):
    item_id: UUID | None = None
    name: str | None = None 
    description: str | None = None
    is_available: bool = None
    amount: int | None = None

class BaseItem(ItemSchema):
    _created_at: date = None
    _last_updated: datetime = None

    class Config:
        from_attributes = True