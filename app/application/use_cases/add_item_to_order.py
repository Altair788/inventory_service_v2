from app.domain.entities import (
    AddItemToOrderRequest,
    AddItemToOrderResponse,
    OrderItem
)
from app.domain.interfaces import (
    ItemRepository,
    OrderRepository,
    OrderItemRepository
)
from app.infrastructure.exceptions import (
    ItemNotFoundException,
    OrderNotFoundException,
    InsufficientStockException,
    BusinessException
)
from app.core.logger import logger


class AddItemToOrderUseCase:
    """Use case for adding items to orders."""

    def __init__(
            self,
            item_repository: ItemRepository,
            order_repository: OrderRepository,
            order_item_repository: OrderItemRepository
    ):
        self.item_repository = item_repository
        self.order_repository = order_repository
        self.order_item_repository = order_item_repository

    async def execute(self, request: AddItemToOrderRequest) -> AddItemToOrderResponse:
        """
        Execute adding item to order.

        Business rules:
        1. Order must exist
        2. Item must exist
        3. Item must have sufficient stock
        4. If item already in order, increment quantity
        5. Update order total amount
        """
        try:
            # Validate order exists
            order = await self.order_repository.get_by_id(request.order_id)
            if not order:
                logger.warning(f"Order not found: {request.order_id}")
                raise OrderNotFoundException(f"Order with ID {request.order_id} not found")

            # Validate item exists
            item = await self.item_repository.get_by_id(request.item_id)
            if not item:
                logger.warning(f"Item not found: {request.item_id}")
                raise ItemNotFoundException(f"Item with ID {request.item_id} not found")

            # Validate sufficient stock
            if item.quantity < request.quantity:
                logger.warning(
                    f"Insufficient stock for item {item.id}. "
                    f"Requested: {request.quantity}, Available: {item.quantity}"
                )
                raise InsufficientStockException(
                    f"Insufficient stock for item {item.name}. "
                    f"Available: {item.quantity}, Requested: {request.quantity}"
                )

            # Check if item already in order
            existing_order_item = await self.order_item_repository.get_by_order_and_item(
                request.order_id,
                request.item_id
            )

            if existing_order_item:
                # Update existing order item quantity
                new_quantity = existing_order_item.quantity + request.quantity
                await self.order_item_repository.update_quantity(
                    existing_order_item.id,
                    new_quantity
                )
                order_item_id = existing_order_item.id
                logger.info(
                    f"Updated existing order item {order_item_id}: "
                    f"quantity {existing_order_item.quantity} -> {new_quantity}"
                )
            else:
                # Create new order item
                order_item = OrderItem(
                    order_id=request.order_id,
                    item_id=request.item_id,
                    quantity=request.quantity,
                    unit_price=item.price
                )
                created_order_item = await self.order_item_repository.create(order_item)
                order_item_id = created_order_item.id
                logger.info(
                    f"Created new order item {order_item_id} for order {request.order_id}"
                )

            # Update item stock
            new_item_quantity = item.quantity - request.quantity
            await self.item_repository.update_quantity(request.item_id, new_item_quantity)
            logger.info(
                f"Updated item {item.id} stock: {item.quantity} -> {new_item_quantity}"
            )

            # Update order total amount
            total_amount = await self._calculate_order_total(request.order_id)
            await self.order_repository.update_total_amount(request.order_id, total_amount)
            logger.info(f"Updated order {request.order_id} total: {total_amount}")

            return AddItemToOrderResponse(
                success=True,
                message="Item successfully added to order",
                order_item_id=order_item_id
            )

        except BusinessException:
            raise
        except Exception as e:
            logger.error(f"Error adding item to order: {e}", exc_info=True)
            raise BusinessException(f"Failed to add item to order: {str(e)}")

    async def _calculate_order_total(self, order_id: int) -> float:
        """Calculate total amount for an order."""
        order_items = await self.order_item_repository.get_by_order_id(order_id)
        total = sum(oi.quantity * float(oi.unit_price) for oi in order_items)
        return total