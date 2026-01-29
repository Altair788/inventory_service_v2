from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Category:
    """Category entity with hierarchical structure."""

    id: Optional[int] = None
    name: str = ""
    parent_id: Optional[int] = None
    level: int = 0
    path: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Item:
    """Item/Nomenclature entity."""

    id: Optional[int] = None
    name: str = ""
    quantity: int = 0
    price: Decimal = Decimal("0.00")
    category_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Client:
    """Client entity."""

    id: Optional[int] = None
    name: str = ""
    address: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Order:
    """Order entity."""

    id: Optional[int] = None
    client_id: int = 0
    status: str = "pending"
    total_amount: Decimal = Decimal("0.00")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class OrderItem:
    """Order item entity (many-to-many relationship)."""

    id: Optional[int] = None
    order_id: int = 0
    item_id: int = 0
    quantity: int = 0
    unit_price: Decimal = Decimal("0.00")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class AddItemToOrderRequest:
    """Request entity for adding item to order."""

    order_id: int
    item_id: int
    quantity: int


@dataclass
class AddItemToOrderResponse:
    """Response entity for adding item to order."""

    success: bool
    message: str
    order_item_id: Optional[int] = None
