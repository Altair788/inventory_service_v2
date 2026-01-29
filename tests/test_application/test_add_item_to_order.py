"""Tests for AddItemToOrder use case."""
import pytest
from decimal import Decimal
from unittest.mock import Mock, AsyncMock

from app.domain.entities import (
    AddItemToOrderRequest,
    AddItemToOrderResponse,
    Item,
    Order,
    OrderItem
)
from app.application.use_cases.add_item_to_order import AddItemToOrderUseCase
from app.infrastructure.exceptions import (
    ItemNotFoundException,
    OrderNotFoundException,
    InsufficientStockException
)


@pytest.mark.asyncio
async def test_add_item_to_order_success():
    """Test successful addition of item to order."""
    # Arrange
    item_repo = Mock()
    order_repo = Mock()
    order_item_repo = Mock()

    # Mock repositories
    item_repo.get_by_id = AsyncMock(return_value=Item(
        id=1, name="Test Item", quantity=10, price=Decimal("100.00")
    ))
    order_repo.get_by_id = AsyncMock(return_value=Order(id=1, client_id=1))
    order_item_repo.get_by_order_and_item = AsyncMock(return_value=None)
    order_item_repo.create = AsyncMock(return_value=OrderItem(
        id=1, order_id=1, item_id=1, quantity=2, unit_price=Decimal("100.00")
    ))
    item_repo.update_quantity = AsyncMock(return_value=True)
    order_repo.update_total_amount = AsyncMock(return_value=True)
    order_item_repo.get_by_order_id = AsyncMock(return_value=[
        OrderItem(id=1, order_id=1, item_id=1, quantity=2, unit_price=Decimal("100.00"))
    ])

    use_case = AddItemToOrderUseCase(item_repo, order_repo, order_item_repo)
    request = AddItemToOrderRequest(order_id=1, item_id=1, quantity=2)

    # Act
    response = await use_case.execute(request)

    # Assert
    assert response.success is True
    assert response.message == "Item successfully added to order"
    assert response.order_item_id == 1
    item_repo.update_quantity.assert_called_once_with(1, 8)  # 10 - 2 = 8


@pytest.mark.asyncio
async def test_add_item_to_order_insufficient_stock():
    """Test adding item with insufficient stock."""
    # Arrange
    item_repo = Mock()
    order_repo = Mock()
    order_item_repo = Mock()

    item_repo.get_by_id = AsyncMock(return_value=Item(
        id=1, name="Test Item", quantity=1, price=Decimal("100.00")
    ))
    order_repo.get_by_id = AsyncMock(return_value=Order(id=1, client_id=1))

    use_case = AddItemToOrderUseCase(item_repo, order_repo, order_item_repo)
    request = AddItemToOrderRequest(order_id=1, item_id=1, quantity=5)

    # Act & Assert
    with pytest.raises(InsufficientStockException):
        await use_case.execute(request)


@pytest.mark.asyncio
async def test_add_item_to_order_not_found():
    """Test adding non-existent item to order."""
    # Arrange
    item_repo = Mock()
    order_repo = Mock()
    order_item_repo = Mock()

    item_repo.get_by_id = AsyncMock(return_value=None)
    order_repo.get_by_id = AsyncMock(return_value=Order(id=1, client_id=1))

    use_case = AddItemToOrderUseCase(item_repo, order_repo, order_item_repo)
    request = AddItemToOrderRequest(order_id=1, item_id=999, quantity=2)

    # Act & Assert
    with pytest.raises(ItemNotFoundException):
        await use_case.execute(request)


@pytest.mark.asyncio
async def test_add_item_to_nonexistent_order():
    """Test adding item to non-existent order."""
    # Arrange
    item_repo = Mock()
    order_repo = Mock()
    order_item_repo = Mock()

    item_repo.get_by_id = AsyncMock(return_value=Item(
        id=1, name="Test Item", quantity=10, price=Decimal("100.00")
    ))
    order_repo.get_by_id = AsyncMock(return_value=None)

    use_case = AddItemToOrderUseCase(item_repo, order_repo, order_item_repo)
    request = AddItemToOrderRequest(order_id=999, item_id=1, quantity=2)

    # Act & Assert
    with pytest.raises(OrderNotFoundException):
        await use_case.execute(request)