from datetime import date, datetime
from fastapi.exceptions import HTTPException

from src.models.items import Item
from src.repositories.item_repository import ItemRepository
from src.schemas.items import ItemCreate
from src.services.auth_service import UserAuthenticationManager

class ItemService:
    '''Item management class. Item-related operations like create, update and others go here'''
    def __init__(self, item_repository: ItemRepository, user_auth_manager: UserAuthenticationManager):
        self.item_repository = item_repository
        self.user_auth_manager = user_auth_manager

    async def create_item(self, item_create: ItemCreate, token: str) -> Item:
        """Create a new Item via item_repository"""
        creator = await self.user_auth_manager.get_current_user(token)

        new_item = Item(
            name=item_create.name,
            description=item_create.description,
            amount=item_create.amount,
            is_available=item_create.is_available,
            _created_by = creator.user_id,
            _created_at=datetime.now(),
            _last_updated=datetime.now()
        )

        return await self.item_repository.create_item(new_item)

    async def get_created_at(self, item: Item) -> date:
        """Return item creation timestamp"""
        return item._created_at

    async def get_last_update(self, item: Item) -> datetime:
        """Return last update timestamp"""
        return item._last_updated

    async def update_last_login(self, item: Item) -> Item:
        """Update last update timestamp"""
        item._last_updated = datetime.now()
        await self.item_repository.update_item(item)

    async def get_item_or_404(self, item_id: UUID) -> Item:
        """Get Item by ID or raise 404 Not Found"""
        item = await self.item_repository.get_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return Item

    async def get_all_items(self) -> list[Item]:
        """Get all existing Item objects from the database"""
        return await self.item_repository.get_all_items()

    async def replace_item(self, item_id: UUID, item: Item) -> Item:
        """Completely replace an existing Item by retrieving it with ID"""
        current_item = await self.get_item_or_404(item_id)
        item.item_id = current_item.item_id
        return await self.item_repository.update_item(item)

    async def update_item(self, item_id: UUID, updated_item: Item) -> Item:
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

        return await self.item_repository.update_item(current_item)

    async def delete_item(self, item_id: UUID) -> dict:
        """Delete Item object by retrieving it with ID"""
        current_item = await self.get_item_or_404(item_id)
        await self.item_repository.delete_item(item_id)
        return {"detail": "Item deleted successfully"}
