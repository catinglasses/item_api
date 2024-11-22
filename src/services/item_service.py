from datetime import date, datetime
from sqlalchemy.orm import Session

from src.models.items import Item
from src.repositories.item_repository import ItemRepository
# from src.schemas.items import ItemCreate

class ItemService:
    '''Item management class. Item-related operations like create, update and others go here'''
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    def create_item(self, item_create: ItemCreate) -> Item:
        """Create a new Item via item_repository"""
        new_item = Item(
            name=item_create.name,
            description=item_create.description,
            amount=item_create.amount,
            is_available=item_create.is_available,
            # TODO: add auto-add creator by ???
            _created_at=datetime.now(),
            _last_updated=datetime.now()
        )
        return self.item_repository.create_item(new_item)

    def get_created_at(self, item: Item):
        """Return item creation timestamp"""
        return item._created_at

    def get_last_update(self, item: Item):
        """Return last update timestamp"""
        return item._last_updated

    def update_last_login(self, item: Item):
        """Update last update timestamp"""
        item._last_updated = datetime.now()
        self.item_repository.update_item(item)