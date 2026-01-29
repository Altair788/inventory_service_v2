from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session
from app.core.logger import logger
from app.infrastructure.database.repositories import SQLAlchemyItemRepository

router = APIRouter()


@router.get(
    "/",
    summary="Get all items",
    description="Retrieve list of all items in the inventory.",
)
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items endpoint."""
    try:
        item_repo = SQLAlchemyItemRepository(session)
        items = await item_repo.get_all()

        return [
            {
                "id": item.id,
                "name": item.name,
                "quantity": item.quantity,
                "price": float(item.price),
                "category_id": item.category_id,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ]

    except Exception as e:
        logger.error(f"Error getting items: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.get(
    "/{item_id}",
    summary="Get item by ID",
    description="Retrieve detailed information about a specific item.",
)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    """Get item by ID endpoint."""
    try:
        item_repo = SQLAlchemyItemRepository(session)
        item = await item_repo.get_by_id(item_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found",
            )

        return {
            "id": item.id,
            "name": item.name,
            "quantity": item.quantity,
            "price": float(item.price),
            "category_id": item.category_id,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting item: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
