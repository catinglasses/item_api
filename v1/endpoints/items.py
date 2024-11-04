from fastapi import FastAPI
from uuid import UUID

from item_api.models.items import Item

app = FastAPI()

# Endpoint to retrieve all items
@app.get("/items/")
async def read_items():
    pass

# Endpoint to retrieve a specific item by its uuid
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: UUID):
    pass

# Endpoint to create a new item
@app.post("/items/create/", response_model=Item)
async def create_item(item: Item):
    pass

# Endpoint to completely replace an existing item by its uuid
@app.put("/items/replace/{item_id}", response_model=Item)
async def replace_item(item_id: UUID, item: Item):
    pass

# Endpoint to partially change an existing item by its uuid
@app.patch("/items/update/{item_id}", response_model=Item)
async def update_item(item_id: UUID, item: Item):
    pass

# Endpoint to delete an item by its uuid
@app.delete("/items/delete/{item_id}")
async def delete_item(item_id: UUID):
    pass