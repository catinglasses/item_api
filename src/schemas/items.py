from fastapi import Query
from pydantic import BaseModel
from datetime import date, datetime

class ItemSchema(BaseModel):
    item_id: int
    name: str
    created_at: date = date.today().isoformat()
    last_updated: datetime = datetime.now().isoformat()
    is_available: bool = True
    amount: int = Query(None, ge=0, le=9999)