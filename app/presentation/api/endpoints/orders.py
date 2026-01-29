from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.add_item_to_order import AddItemToOrderUseCase
from app.core.dependencies import get_session
from app.core.logger import logger
from app.domain.entities import AddItemToOrderRequest
from app.infrastructure.database.repositories import (
    SQLAlchemyItemRepository,
    SQLAlchemyOrderItemRepository,
    SQLAlchemyOrderRepository,
)
from app.infrastructure.exceptions import (
    BusinessException,
    InsufficientStockException,
    ItemNotFoundException,
    OrderNotFoundException,
)

router = APIRouter()


class AddItemToOrderRequestSchema(BaseModel):
    """Request schema for adding item to order."""

    order_id: int = Field(..., description="ID of the order", gt=0)
    item_id: int = Field(..., description="ID of the item", gt=0)
    quantity: int = Field(..., description="Quantity of items to add", gt=0, le=1000)

    class Config:
        json_schema_extra = {"example": {"order_id": 1, "item_id": 5, "quantity": 2}}


@router.post(
    "/{order_id}/items",
    status_code=status.HTTP_201_CREATED,
    summary="Add item to order",
    description="""
    Add an item to an existing order. If the item already exists in the order,
    the quantity will be incremented. The item's stock will be reduced accordingly.

    Business rules:
    - Order must exist
    - Item must exist  
    - Item must have sufficient stock
    - If item already in order, increment quantity
    - Update order total amount automatically
    """,
)
async def add_item_to_order(
    order_id: int,
    request: AddItemToOrderRequestSchema,  # ← Теперь это РАБОТАЕТ!
    session: AsyncSession = Depends(get_session),
):
    """
    Add item to order endpoint.

    Args:
        order_id: ID of the order from path
        request: Request body with item_id and quantity
        session: Database session

    Returns:
        Success response with order_item_id

    Raises:
        HTTP 404: Order or item not found
        HTTP 400: Insufficient stock or business logic error
        HTTP 500: Internal server error
    """
    try:
        # Validate order_id from path matches order_id from body
        if request.order_id != order_id:
            logger.warning(
                f"Path order_id ({order_id}) doesn't match body order_id ({request.order_id})"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Order ID mismatch: path={order_id}, body={request.order_id}",
            )

        # Create repositories
        order_repo = SQLAlchemyOrderRepository(session)
        item_repo = SQLAlchemyItemRepository(session)
        order_item_repo = SQLAlchemyOrderItemRepository(session)

        # Create use case
        use_case = AddItemToOrderUseCase(
            item_repository=item_repo,
            order_repository=order_repo,
            order_item_repository=order_item_repo,
        )

        # Execute use case
        domain_request = AddItemToOrderRequest(
            order_id=request.order_id,
            item_id=request.item_id,
            quantity=request.quantity,
        )

        response = await use_case.execute(domain_request)

        logger.info(
            f"Successfully added item {request.item_id} " f"to order {request.order_id}"
        )

        return {
            "success": response.success,
            "message": response.message,
            "order_item_id": response.order_item_id,
        }

    except OrderNotFoundException as e:
        logger.warning(f"Order not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ItemNotFoundException as e:
        logger.warning(f"Item not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InsufficientStockException as e:
        logger.warning(f"Insufficient stock: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except BusinessException as e:
        logger.error(f"Business error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.get(
    "/{order_id}",
    summary="Get order details",
    description="Retrieve detailed information about a specific order including all items.",
)
async def get_order(order_id: int, session: AsyncSession = Depends(get_session)):
    """Get order details endpoint."""
    try:
        order_repo = SQLAlchemyOrderRepository(session)
        order = await order_repo.get_by_id(order_id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with ID {order_id} not found",
            )

        # Get order items
        order_item_repo = SQLAlchemyOrderItemRepository(session)
        order_items = await order_item_repo.get_by_order_id(order_id)

        return {
            "id": order.id,
            "client_id": order.client_id,
            "status": order.status,
            "total_amount": float(order.total_amount),
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "items": [
                {
                    "id": oi.id,
                    "item_id": oi.item_id,
                    "quantity": oi.quantity,
                    "unit_price": float(oi.unit_price),
                    "created_at": oi.created_at,
                }
                for oi in order_items
            ],
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting order: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
