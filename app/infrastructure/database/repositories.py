from decimal import Decimal
from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Category, Client, Item, Order, OrderItem
from app.domain.interfaces import (
    CategoryRepository,
    ClientRepository,
    ItemRepository,
    OrderItemRepository,
    OrderRepository,
)
from app.infrastructure.database.models import (
    CategoryModel,
    ClientModel,
    ItemModel,
    OrderItemModel,
    OrderModel,
)


class SQLAlchemyCategoryRepository(CategoryRepository):
    """SQLAlchemy implementation of CategoryRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, category: Category) -> Category:
        db_category = CategoryModel(
            name=category.name,
            parent_id=category.parent_id,
            level=category.level,
            path=category.path,
        )
        self.session.add(db_category)
        await self.session.flush()
        await self.session.refresh(db_category)

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return Category(
            id=db_category.id,
            name=db_category.name,
            parent_id=db_category.parent_id,
            level=db_category.level,
            path=db_category.path,
            created_at=db_category.created_at,
            updated_at=db_category.updated_at,
        )

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        db_category = result.scalar_one_or_none()

        if db_category:
            return Category(
                id=db_category.id,
                name=db_category.name,
                parent_id=db_category.parent_id,
                level=db_category.level,
                path=db_category.path,
                created_at=db_category.created_at,
                updated_at=db_category.updated_at,
            )
        return None

    async def get_all(self) -> List[Category]:
        result = await self.session.execute(select(CategoryModel))
        db_categories = result.scalars().all()

        return [
            Category(
                id=c.id,
                name=c.name,
                parent_id=c.parent_id,
                level=c.level,
                path=c.path,
                created_at=c.created_at,
                updated_at=c.updated_at,
            )
            for c in db_categories
        ]

    async def get_children(self, parent_id: Optional[int]) -> List[Category]:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.parent_id == parent_id)
        )
        db_categories = result.scalars().all()

        return [
            Category(
                id=c.id,
                name=c.name,
                parent_id=c.parent_id,
                level=c.level,
                path=c.path,
                created_at=c.created_at,
                updated_at=c.updated_at,
            )
            for c in db_categories
        ]

    async def update(self, category: Category) -> Category:
        await self.session.execute(
            update(CategoryModel)
            .where(CategoryModel.id == category.id)
            .values(
                name=category.name,
                parent_id=category.parent_id,
                level=category.level,
                path=category.path,
            )
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return await self.get_by_id(category.id)

    async def delete(self, category_id: int) -> bool:
        result = await self.session.execute(
            delete(CategoryModel).where(CategoryModel.id == category_id)
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return result.rowcount > 0


class SQLAlchemyItemRepository(ItemRepository):
    """SQLAlchemy implementation of ItemRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, item: Item) -> Item:
        db_item = ItemModel(
            name=item.name,
            quantity=item.quantity,
            price=item.price,
            category_id=item.category_id,
        )
        self.session.add(db_item)
        await self.session.flush()
        await self.session.refresh(db_item)

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return Item(
            id=db_item.id,
            name=db_item.name,
            quantity=db_item.quantity,
            price=db_item.price,
            category_id=db_item.category_id,
            created_at=db_item.created_at,
            updated_at=db_item.updated_at,
        )

    async def get_by_id(self, item_id: int) -> Optional[Item]:
        result = await self.session.execute(
            select(ItemModel).where(ItemModel.id == item_id)
        )
        db_item = result.scalar_one_or_none()

        if db_item:
            return Item(
                id=db_item.id,
                name=db_item.name,
                quantity=db_item.quantity,
                price=db_item.price,
                category_id=db_item.category_id,
                created_at=db_item.created_at,
                updated_at=db_item.updated_at,
            )
        return None

    async def get_all(self) -> List[Item]:
        result = await self.session.execute(select(ItemModel))
        db_items = result.scalars().all()

        return [
            Item(
                id=i.id,
                name=i.name,
                quantity=i.quantity,
                price=i.price,
                category_id=i.category_id,
                created_at=i.created_at,
                updated_at=i.updated_at,
            )
            for i in db_items
        ]

    async def update(self, item: Item) -> Item:
        await self.session.execute(
            update(ItemModel)
            .where(ItemModel.id == item.id)
            .values(
                name=item.name,
                quantity=item.quantity,
                price=item.price,
                category_id=item.category_id,
            )
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return await self.get_by_id(item.id)

    async def update_quantity(self, item_id: int, quantity: int) -> bool:
        result = await self.session.execute(
            update(ItemModel).where(ItemModel.id == item_id).values(quantity=quantity)
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return result.rowcount > 0

    async def delete(self, item_id: int) -> bool:
        result = await self.session.execute(
            delete(ItemModel).where(ItemModel.id == item_id)
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return result.rowcount > 0


class SQLAlchemyClientRepository(ClientRepository):
    """SQLAlchemy implementation of ClientRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, client: Client) -> Client:
        db_client = ClientModel(name=client.name, address=client.address)
        self.session.add(db_client)
        await self.session.flush()
        await self.session.refresh(db_client)

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return Client(
            id=db_client.id,
            name=db_client.name,
            address=db_client.address,
            created_at=db_client.created_at,
            updated_at=db_client.updated_at,
        )

    async def get_by_id(self, client_id: int) -> Optional[Client]:
        result = await self.session.execute(
            select(ClientModel).where(ClientModel.id == client_id)
        )
        db_client = result.scalar_one_or_none()

        if db_client:
            return Client(
                id=db_client.id,
                name=db_client.name,
                address=db_client.address,
                created_at=db_client.created_at,
                updated_at=db_client.updated_at,
            )
        return None

    async def get_all(self) -> List[Client]:
        result = await self.session.execute(select(ClientModel))
        db_clients = result.scalars().all()

        return [
            Client(
                id=c.id,
                name=c.name,
                address=c.address,
                created_at=c.created_at,
                updated_at=c.updated_at,
            )
            for c in db_clients
        ]

    async def update(self, client: Client) -> Client:
        await self.session.execute(
            update(ClientModel)
            .where(ClientModel.id == client.id)
            .values(name=client.name, address=client.address)
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return await self.get_by_id(client.id)

    async def delete(self, client_id: int) -> bool:
        result = await self.session.execute(
            delete(ClientModel).where(ClientModel.id == client_id)
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return result.rowcount > 0


class SQLAlchemyOrderRepository(OrderRepository):
    """SQLAlchemy implementation of OrderRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, order: Order) -> Order:
        db_order = OrderModel(
            client_id=order.client_id,
            status=order.status,
            total_amount=order.total_amount,
        )
        self.session.add(db_order)
        await self.session.flush()
        await self.session.refresh(db_order)

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return Order(
            id=db_order.id,
            client_id=db_order.client_id,
            status=db_order.status,
            total_amount=db_order.total_amount,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at,
        )

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        result = await self.session.execute(
            select(OrderModel).where(OrderModel.id == order_id)
        )
        db_order = result.scalar_one_or_none()

        if db_order:
            return Order(
                id=db_order.id,
                client_id=db_order.client_id,
                status=db_order.status,
                total_amount=db_order.total_amount,
                created_at=db_order.created_at,
                updated_at=db_order.updated_at,
            )
        return None

    async def get_all(self) -> List[Order]:
        result = await self.session.execute(select(OrderModel))
        db_orders = result.scalars().all()

        return [
            Order(
                id=o.id,
                client_id=o.client_id,
                status=o.status,
                total_amount=o.total_amount,
                created_at=o.created_at,
                updated_at=o.updated_at,
            )
            for o in db_orders
        ]

    async def update(self, order: Order) -> Order:
        await self.session.execute(
            update(OrderModel)
            .where(OrderModel.id == order.id)
            .values(
                client_id=order.client_id,
                status=order.status,
                total_amount=order.total_amount,
            )
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return await self.get_by_id(order.id)

    async def update_total_amount(self, order_id: int, amount: Decimal) -> bool:
        result = await self.session.execute(
            update(OrderModel)
            .where(OrderModel.id == order_id)
            .values(total_amount=amount)
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return result.rowcount > 0

    async def delete(self, order_id: int) -> bool:
        result = await self.session.execute(
            delete(OrderModel).where(OrderModel.id == order_id)
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return result.rowcount > 0


class SQLAlchemyOrderItemRepository(OrderItemRepository):
    """SQLAlchemy implementation of OrderItemRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, order_item: OrderItem) -> OrderItem:
        db_order_item = OrderItemModel(
            order_id=order_item.order_id,
            item_id=order_item.item_id,
            quantity=order_item.quantity,
            unit_price=order_item.unit_price,
        )
        self.session.add(db_order_item)
        await self.session.flush()
        await self.session.refresh(db_order_item)

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return OrderItem(
            id=db_order_item.id,
            order_id=db_order_item.order_id,
            item_id=db_order_item.item_id,
            quantity=db_order_item.quantity,
            unit_price=db_order_item.unit_price,
            created_at=db_order_item.created_at,
            updated_at=db_order_item.updated_at,
        )

    async def get_by_id(self, order_item_id: int) -> Optional[OrderItem]:
        result = await self.session.execute(
            select(OrderItemModel).where(OrderItemModel.id == order_item_id)
        )
        db_order_item = result.scalar_one_or_none()

        if db_order_item:
            return OrderItem(
                id=db_order_item.id,
                order_id=db_order_item.order_id,
                item_id=db_order_item.item_id,
                quantity=db_order_item.quantity,
                unit_price=db_order_item.unit_price,
                created_at=db_order_item.created_at,
                updated_at=db_order_item.updated_at,
            )
        return None

    async def get_by_order_id(self, order_id: int) -> List[OrderItem]:
        result = await self.session.execute(
            select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        )
        db_order_items = result.scalars().all()

        return [
            OrderItem(
                id=oi.id,
                order_id=oi.order_id,
                item_id=oi.item_id,
                quantity=oi.quantity,
                unit_price=oi.unit_price,
                created_at=oi.created_at,
                updated_at=oi.updated_at,
            )
            for oi in db_order_items
        ]

    async def get_by_order_and_item(
            self, order_id: int, item_id: int
    ) -> Optional[OrderItem]:
        result = await self.session.execute(
            select(OrderItemModel)
            .where(OrderItemModel.order_id == order_id)
            .where(OrderItemModel.item_id == item_id)
        )
        db_order_item = result.scalar_one_or_none()

        if db_order_item:
            return OrderItem(
                id=db_order_item.id,
                order_id=db_order_item.order_id,
                item_id=db_order_item.item_id,
                quantity=db_order_item.quantity,
                unit_price=db_order_item.unit_price,
                created_at=db_order_item.created_at,
                updated_at=db_order_item.updated_at,
            )
        return None

    async def update_quantity(self, order_item_id: int, quantity: int) -> bool:
        result = await self.session.execute(
            update(OrderItemModel)
            .where(OrderItemModel.id == order_item_id)
            .values(quantity=quantity)
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return result.rowcount > 0

    async def delete(self, order_item_id: int) -> bool:
        result = await self.session.execute(
            delete(OrderItemModel).where(OrderItemModel.id == order_item_id)
        )
        await self.session.flush()

        # 🔑 Сохраняем изменения в БД
        await self.session.commit()

        return result.rowcount > 0