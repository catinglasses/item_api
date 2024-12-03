from fastapi import Query
from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID

class ItemSchema(BaseModel):
    item_id: int
    name: str
    description: str | None = None
    _created_at: date = date.today().isoformat()
    _last_updated: datetime = datetime.now().isoformat()
    is_available: bool | None = None
    amount: int = Query(None, ge=0, le=9999)
    _created_by: UUID

class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    amount: int | None = 0
    is_available: bool | None = False

class ItemPatchSchema(ItemSchema):
    item_id: int | None = None
    name: str | None = None
    is_available: bool = True
