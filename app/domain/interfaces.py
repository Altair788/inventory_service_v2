from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional, Protocol

from app.domain.entities import (
    AddItemToOrderRequest,
    AddItemToOrderResponse,
    Category,
    Client,
    Item,
    Order,
    OrderItem,
)


class Repository(Protocol):
    """Base repository protocol."""

    pass


class CategoryRepository(ABC):
    """Abstract repository for categories."""

    @abstractmethod
    async def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def get_by_id(self, category_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Category]:
        pass

    @abstractmethod
    async def get_children(self, parent_id: Optional[int]) -> List[Category]:
        pass

    @abstractmethod
    async def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def delete(self, category_id: int) -> bool:
        pass


class ItemRepository(ABC):
    """Abstract repository for items."""

    @abstractmethod
    async def create(self, item: Item) -> Item:
        pass

    @abstractmethod
    async def get_by_id(self, item_id: int) -> Optional[Item]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Item]:
        pass

    @abstractmethod
    async def update(self, item: Item) -> Item:
        pass

    @abstractmethod
    async def update_quantity(self, item_id: int, quantity: int) -> bool:
        pass

    @abstractmethod
    async def delete(self, item_id: int) -> bool:
        pass


class ClientRepository(ABC):
    """Abstract repository for clients."""

    @abstractmethod
    async def create(self, client: Client) -> Client:
        pass

    @abstractmethod
    async def get_by_id(self, client_id: int) -> Optional[Client]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Client]:
        pass

    @abstractmethod
    async def update(self, client: Client) -> Client:
        pass

    @abstractmethod
    async def delete(self, client_id: int) -> bool:
        pass


class OrderRepository(ABC):
    """Abstract repository for orders."""

    @abstractmethod
    async def create(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Order]:
        pass

    @abstractmethod
    async def update(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def update_total_amount(self, order_id: int, amount: Decimal) -> bool:
        pass

    @abstractmethod
    async def delete(self, order_id: int) -> bool:
        pass


class OrderItemRepository(ABC):
    """Abstract repository for order items."""

    @abstractmethod
    async def create(self, order_item: OrderItem) -> OrderItem:
        pass

    @abstractmethod
    async def get_by_id(self, order_item_id: int) -> Optional[OrderItem]:
        pass

    @abstractmethod
    async def get_by_order_id(self, order_id: int) -> List[OrderItem]:
        pass

    @abstractmethod
    async def get_by_order_and_item(
        self, order_id: int, item_id: int
    ) -> Optional[OrderItem]:
        pass

    @abstractmethod
    async def update_quantity(self, order_item_id: int, quantity: int) -> bool:
        pass

    @abstractmethod
    async def delete(self, order_item_id: int) -> bool:
        pass


class AddItemToOrderService(ABC):
    """Abstract service for adding items to orders."""

    @abstractmethod
    async def execute(self, request: AddItemToOrderRequest) -> AddItemToOrderResponse:
        pass
