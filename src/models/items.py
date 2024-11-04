from sqlalchemy import Column, Uuid, Integer, String, Boolean, Date, DateTime

from src.models.database import Base

class Item(Base):
    __tablename__ = "Item"

    item_id = Column(Uuid, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(Date, nullable=False)
    last_updated = Column(DateTime, nullable=False)
    is_available = Column(Boolean, default=False)
    amount = Column(Integer, default=0)
    created_by = Column(models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE))