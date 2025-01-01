from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends

from src.models.users import User
from src.models.items import Item
from src.services.item_service import ItemService
from src.dependencies import get_item_service, get_current_user
from src.schemas.items import ItemSchema, ItemCreate, ItemPatchSchema, BaseItem

router = APIRouter(tags=["items"])

# Endpoint to retrieve all items
@router.get("/", response_model=List[BaseItem])
async def read_items(item_service: ItemService = Depends(get_item_service)):
    items = await item_service.get_all_items()
    return items

# Endpoint to retrieve a specific item by its uuid
@router.get("/{item_id}", response_model=BaseItem)
async def read_item(item_id: UUID, item_service: ItemService = Depends(get_item_service)):
    return await item_service.get_item_or_404(item_id)

# Endpoint to create a new item
@router.post("/create", response_model=BaseItem)
async def create_item(
    item_create: ItemCreate,
    item_service: ItemService = Depends(get_item_service),
    creator: User = Depends(get_current_user)
):
    creator_id = creator.user_id
    return await item_service.create_item(item_create, creator_id)

# Endpoint to completely replace an existing item by its uuid
@router.put("/replace/{item_id}", response_model=BaseItem)
async def replace_item(
    item_id: UUID,
    item: ItemSchema,
    item_service: ItemService = Depends(get_item_service)
):
    existing_item = await item_service.get_item_or_404(item_id)
    item.item_id = existing_item.item_id
    return await item_service.replace_item(item_id, item)

# Endpoint to partially change an existing item by its uuid
@router.patch("/update/{item_id}", response_model=BaseItem)
async def update_item(
    item_id: UUID,
    updated_item: ItemPatchSchema,
    item_service: ItemService = Depends(get_item_service)
):
    return await item_service.update_item(item_id, updated_item)

# Endpoint to delete an item by its uuid
@router.delete("/delete/{item_id}")
async def delete_item(
    item_id: UUID,
    item_service: ItemService = Depends(get_item_service)
):
    await item_service.delete_item(item_id)
    return {"detail": f"Item {item_id} deleted successfully"}
