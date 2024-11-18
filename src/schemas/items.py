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
    is_available: bool = True
    amount: int = Query(None, ge=0, le=9999)
    _created_by: UUID