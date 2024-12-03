from fastapi import APIRouter
from v1.endpoints.items import router as items_router
from v1.endpoints.users import router as users_router

api_router = APIRouter()

api_router.include_router(items_router, prefix="/items", tags=["items"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
