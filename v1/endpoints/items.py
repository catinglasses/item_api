from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from src.models.items import Item
from src.models.database import get_db
from src.schemas.items import ItemCreate
from src.services.item_service import ItemService
from src.repositories.item_repository import ItemRepository
from src.dependencies import get_item_service, get_current_user

router = APIRouter(tags=["items"])

# Endpoint to retrieve all items
@router.get("/items/", response_model=List[Item])
async def read_items(item_service: ItemService = Depends(get_item_service)):
    items = await item_service.get_all_items()
    return items

# Endpoint to retrieve a specific item by its uuid
@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: UUID, item_service: ItemService = Depends(get_item_service)):
    return await item_service.get_item_or_404(item_id)

# Endpoint to create a new item
@router.post("/items/create/", response_model=Item)
async def create_item(
    item_create: ItemCreate,
    item_service: ItemService = Depends(get_item_service),
    creator_id: UUID = Depends(get_current_user)
):
    return await item_service.create_item(item_create, creator_id)

# Endpoint to completely replace an existing item by its uuid
@router.put("/items/replace/{item_id}", response_model=Item)
async def replace_item(
    item_id: UUID,
    item: Item,
    item_service: ItemService = Depends(get_item_service)
):
    existing_item = await item_service.get_item_or_404(item_id)
    item.item_id = item_id
    return await item_repository.update_item(item)

# Endpoint to partially change an existing item by its uuid
@router.patch("/items/update/{item_id}", response_model=Item)
async def update_item(
    item_id: UUID,
    updated_item: Item,
    item_service: ItemService = Depends(get_item_service)
):
    return await item_service.update_item(item_id, updated_item)

# Endpoint to delete an item by its uuid
@router.delete("/items/delete/{item_id}")
async def delete_item(
    item_id: UUID,
    item_service: ItemService = Depends(get_item_service)
):
    item_service.delete_item(item_id)
    return {"detail": f"Item {item_id} deleted successfully"}
