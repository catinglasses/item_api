from uuid import UUID
from datetime import date, datetime
from fastapi.exceptions import HTTPException

from src.models.items import Item
from src.repositories.item_repository import ItemRepository
from src.schemas.items import ItemSchema, ItemCreate, ItemPatchSchema, BaseItem

class ItemService:
    '''Item management class. Item-related operations like create, update and others go here'''
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    async def create_item(self, item_create: ItemCreate, creator_id: UUID) -> Item:
        """Create a new Item via item_repository"""

        new_item = Item(
            name=item_create.name,
            description=item_create.description,
            amount=item_create.amount,
            is_available=item_create.is_available,
            _created_by = creator_id,
            _created_at=datetime.now(),
            _last_updated=datetime.now()
        )

        return await self.item_repository.create_item(new_item)

    async def get_created_at(self, item: BaseItem) -> date:
        """Return item creation timestamp"""
        return item._created_at

    async def get_last_update(self, item: BaseItem) -> datetime:
        """Return last update timestamp"""
        return item._last_updated

# DEPRECATED since it's easier to manually set new value when actually updating items
    # async def update_last_updated(self, item: Item) -> Item:
    #     """Update last update timestamp"""
    #     item._last_updated = datetime.now()
    #     await self.item_repository.update_item(item)

    async def get_item_or_404(self, item_id: UUID) -> Item:
        """Get Item by ID or raise 404 Not Found"""
        item = await self.item_repository.get_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
        # return BaseItem.model_validate(item)

    async def get_all_items(self) -> list[Item]:
        """Get all existing Item objects from the database"""
        return await self.item_repository.get_all_items()

    async def replace_item(self, item_id: UUID, item: ItemSchema) -> Item:
        """Completely replace an existing Item by retrieving it with ID"""
        current_item = await self.get_item_or_404(item_id)

        current_item.name = item.name
        current_item.description = item.description
        current_item.amount = item.amount
        current_item.is_available = item.is_available
        current_item._last_updated = datetime.now()
        
        return await self.item_repository.update_item(item)

    async def update_item(self, item_id: UUID, updated_item: ItemPatchSchema) -> Item:
        """Partially change an existing Item by retrieving it with ID"""
        current_item = await self.get_item_or_404(item_id)

        if updated_item.name is not None:
            current_item.name = updated_item.name
        if updated_item.description is not None:
            current_item.description = updated_item.description
        if updated_item.amount is not None:
            current_item.amount = updated_item.amount
        if updated_item.is_available is not None:
            current_item.is_available = updated_item.is_available
        current_item._last_updated = datetime.now()

        return await self.item_repository.update_item(current_item)

    async def delete_item(self, item_id: UUID) -> dict:
        """Delete Item object by retrieving it with ID"""
        await self.item_repository.delete_item(item_id)
        return {"detail": "Item deleted successfully"}
