from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session
from app.core.logger import logger
from app.infrastructure.database.repositories import SQLAlchemyCategoryRepository

router = APIRouter()


@router.get(
    "/",
    summary="Get all categories",
    description="Retrieve hierarchical list of all categories.",
)
async def get_categories(session: AsyncSession = Depends(get_session)):
    """Get all categories endpoint."""
    try:
        category_repo = SQLAlchemyCategoryRepository(session)
        categories = await category_repo.get_all()

        return [
            {
                "id": category.id,
                "name": category.name,
                "parent_id": category.parent_id,
                "level": category.level,
                "path": category.path,
                "created_at": category.created_at,
                "updated_at": category.updated_at,
            }
            for category in categories
        ]

    except Exception as e:
        logger.error(f"Error getting categories: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.get(
    "/{category_id}",
    summary="Get category by ID",
    description="Retrieve detailed information about a specific category.",
)
async def get_category(category_id: int, session: AsyncSession = Depends(get_session)):
    """Get category by ID endpoint."""
    try:
        category_repo = SQLAlchemyCategoryRepository(session)
        category = await category_repo.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found",
            )

        return {
            "id": category.id,
            "name": category.name,
            "parent_id": category.parent_id,
            "level": category.level,
            "path": category.path,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting category: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
