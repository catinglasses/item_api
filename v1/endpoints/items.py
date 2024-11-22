from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List

from src.models.items import Item
from src.repositories.item_repository import ItemRepository
from src.models.database import get_db

router = APIRouter(tags=["items"])

# Dependency Injection to get the database session via repository pattern
async def get_item_repository(db: AsyncSession = Depends(get_db)) -> ItemRepository:
    return ItemRepository(db)

async def get_item_or_404(item_id: UUID, item_repository: ItemRepository = Depends(get_item_repository)):
    item = await item_repository.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item

# Endpoint to retrieve all items
@router.get("/items/", response_model=List[Item])
async def read_items(item_repository: ItemRepository = Depends(get_item_repository)):
    items = await item_repository.get_all_items() # TODO: implement this in repo and service
    return items

# Endpoint to retrieve a specific item by its uuid
@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: UUID, item_repository: ItemRepository = Depends(get_item_repository)):
    return await get_item_or_404(item_id, item_repository)

# Endpoint to create a new item
@router.post("/items/create/", response_model=Item)
async def create_item(item: Item, item_repository: ItemRepository = Depends(get_item_repository)):
    return await item_repository.create_item(item)

# Endpoint to completely replace an existing item by its uuid
@router.put("/items/replace/{item_id}", response_model=Item)
async def replace_item(item_id: UUID, item: Item, item_repository: ItemRepository = Depends(get_item_repository)):
    existing_item = await get_item_or_404(item_id, item_repository)
    item.item_id = item_id
    return await item_repository.update_item(item)

# Endpoint to partially change an existing item by its uuid
@router.patch("/items/update/{item_id}", response_model=Item)
async def update_item(item_id: UUID, updated_item: Item, item_repository: ItemRepository = Depends(get_item_repository)):
    existing_item = await get_item_or_404(item_id, item_repository)

    if updated_item.name is not None:
        existing_item.name = updated_item.name
    if updated_item.description is not None:
        existing_item.description = updated_item.description
    if updated_item.amount is not None:
        existing_item.amount = updated_item.amount
    if updated_item.is_available is not None:
        existing_item.is_available = updated_item.is_available

    return await item_repository.update_item(existing_item)

# Endpoint to delete an item by its uuid
@router.delete("/items/delete/{item_id}")
async def delete_item(item_id: UUID, item_repository: ItemRepository = Depends(get_item_repository)):
    existing_item = await get_item_or_404(item_id, item_repository)
    await item_repository.delete_item(item_id) #TODO: implement in ItemRepository & ItemService
    return {"detail": "Item deleted successfully"}
