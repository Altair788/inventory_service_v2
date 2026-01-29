from fastapi import APIRouter

from app.presentation.api.endpoints import categories, items, orders

api_router = APIRouter()

api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
