from sqlalchemy import Uuid, select
from sqlalchemy.orm import Session

from src.models.items import Item

class ItemRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_item(self, item_data: Item) -> Item:
        self.db_session.add(item_data)
        self.db_session.commit()
        self.db_session.refresh(_data)
        return item_data

    def update_item(self, item_data: Item) -> Item:
        """Update existing item in the db"""
        self.db_session.commit()
        return item_data

    def _get_item(self, criteria) -> Item:
        """Private method to retrieve a item based on a given criteria"""
        stmt = select(Item).where(criteria)
        result = self.db_session.execute(stmt).scalars().one_or_none()
        if result is None:
            raise NoResultFound("Item not found")

    def get_item_by_id(self, item_id: Uuid) -> Item:
        return self._get_item(Item.item_id == item_id)

    def get_item_by_name(self, item_name: str) -> Item:
        return self._get_item(Item.name == item_name)
