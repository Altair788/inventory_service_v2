#!/usr/bin/env python3
"""
Скрипт для заполнения базы тестовыми данными.
Работает в любом окружении: локально, в контейнере, из любой директории.
"""
import sys
import asyncio
from pathlib import Path
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


# 🔑 Автоматическое определение корня проекта
def find_project_root() -> Path:
    """Найти корень проекта (директорию с pyproject.toml)"""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    raise RuntimeError("Не удалось найти корень проекта (нет pyproject.toml)")


# Добавляем корень проекта в sys.path
project_root = find_project_root()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Теперь импортируем модули приложения
from app.core.database import engine
from app.infrastructure.database.models import (
    CategoryModel,
    ItemModel,
    ClientModel,
    OrderModel,
)


async def seed_data():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        print("🌱 Проверяем наличие данных в базе...")

        # 🔑 Защита от дубликатов: проверяем, есть ли уже данные
        category_count = await session.scalar(select(func.count()).select_from(CategoryModel))
        item_count = await session.scalar(select(func.count()).select_from(ItemModel))
        client_count = await session.scalar(select(func.count()).select_from(ClientModel))

        if category_count > 0 or item_count > 0 or client_count > 0:
            print(
                f"⚠️  База уже содержит данные (категории: {category_count}, товары: {item_count}, клиенты: {client_count}). Пропускаем наполнение.")
            return

        print("✅ База пуста. Заполняем тестовыми данными...")

        # === Категории ===
        print("\n📁 Создаём категории...")

        # Корневые категории
        electronics = CategoryModel(
            name="Бытовая техника", parent_id=None, level=0, path="/1/"
        )
        computers = CategoryModel(
            name="Компьютеры", parent_id=None, level=0, path="/2/"
        )
        session.add_all([electronics, computers])
        await session.flush()
        print(f"   ✅ Бытовая техника (ID={electronics.id})")
        print(f"   ✅ Компьютеры (ID={computers.id})")

        # Подкатегории бытовой техники
        washing_machines = CategoryModel(
            name="Стиральные машины",
            parent_id=electronics.id,
            level=1,
            path=f"/1/{electronics.id}/",
        )
        refrigerators = CategoryModel(
            name="Холодильники",
            parent_id=electronics.id,
            level=1,
            path=f"/1/{electronics.id}/",
        )
        tvs = CategoryModel(
            name="Телевизоры",
            parent_id=electronics.id,
            level=1,
            path=f"/1/{electronics.id}/",
        )
        session.add_all([washing_machines, refrigerators, tvs])
        await session.flush()
        print(f"   ✅ Стиральные машины (ID={washing_machines.id})")
        print(f"   ✅ Холодильники (ID={refrigerators.id})")
        print(f"   ✅ Телевизоры (ID={tvs.id})")

        # Подкатегории компьютеров
        laptops = CategoryModel(
            name="Ноутбуки",
            parent_id=computers.id,
            level=1,
            path=f"/2/{computers.id}/",
        )
        monoblocks = CategoryModel(
            name="Моноблоки",
            parent_id=computers.id,
            level=1,
            path=f"/2/{computers.id}/",
        )
        session.add_all([laptops, monoblocks])
        await session.flush()
        print(f"   ✅ Ноутбуки (ID={laptops.id})")
        print(f"   ✅ Моноблоки (ID={monoblocks.id})")

        # Подподкатегории
        laptops_17 = CategoryModel(
            name='17"',
            parent_id=laptops.id,
            level=2,
            path=f"/2/{computers.id}/{laptops.id}/",
        )
        laptops_19 = CategoryModel(
            name='19"',
            parent_id=laptops.id,
            level=2,
            path=f"/2/{computers.id}/{laptops.id}/",
        )
        session.add_all([laptops_17, laptops_19])
        await session.flush()
        print(f"   ✅ Ноутбуки 17\" (ID={laptops_17.id})")
        print(f"   ✅ Ноутбуки 19\" (ID={laptops_19.id})")

        # === Товары ===
        print("\n📦 Создаём товары...")
        items = [
            ItemModel(
                name="Стиральная машина LG F1073QD",
                quantity=15,
                price=Decimal("24990.00"),
                category_id=washing_machines.id,
            ),
            ItemModel(
                name="Стиральная машина Samsung WW60J42G",
                quantity=8,
                price=Decimal("32500.00"),
                category_id=washing_machines.id,
            ),
            ItemModel(
                name="Холодильник Samsung RB38T600ESL",
                quantity=12,
                price=Decimal("45990.00"),
                category_id=refrigerators.id,
            ),
            ItemModel(
                name="Холодильник LG GA-B409SLTL",
                quantity=6,
                price=Decimal("38700.00"),
                category_id=refrigerators.id,
            ),
            ItemModel(
                name="Телевизор Samsung UE55AU7100U",
                quantity=20,
                price=Decimal("39990.00"),
                category_id=tvs.id,
            ),
            ItemModel(
                name="Ноутбук Dell XPS 15 9520",
                quantity=10,
                price=Decimal("129990.00"),
                category_id=laptops.id,
            ),
            ItemModel(
                name="Ноутбук HP Pavilion 15",
                quantity=18,
                price=Decimal("59990.00"),
                category_id=laptops.id,
            ),
            ItemModel(
                name="Моноблок Apple iMac 24\"",
                quantity=5,
                price=Decimal("119990.00"),
                category_id=monoblocks.id,
            ),
        ]
        session.add_all(items)
        await session.flush()
        for i, item in enumerate(items, 1):
            print(f"   ✅ {i}. {item.name} (ID={item.id}, остаток={item.quantity})")

        # === Клиенты ===
        print("\n👤 Создаём клиентов...")
        client1 = ClientModel(
            name="ООО 'Ромашка'", address="г. Москва, ул. Тверская, д. 15, офис 301"
        )
        client2 = ClientModel(
            name="ИП Петров А.В.", address="г. Санкт-Петербург, Невский пр., д. 28"
        )
        session.add_all([client1, client2])
        await session.flush()
        print(f"   ✅ ООО 'Ромашка' (ID={client1.id})")
        print(f"   ✅ ИП Петров А.В. (ID={client2.id})")

        # === Заказы ===
        print("\n📋 Создаём заказы...")
        order1 = OrderModel(
            client_id=client1.id, status="pending", total_amount=Decimal("0.00")
        )
        order2 = OrderModel(
            client_id=client2.id, status="pending", total_amount=Decimal("0.00")
        )
        session.add_all([order1, order2])
        await session.flush()
        print(f"   ✅ Заказ №{order1.id} для ООО 'Ромашка'")
        print(f"   ✅ Заказ №{order2.id} для ИП Петров А.В.")

        # Фиксируем все изменения
        await session.commit()
        print("\n✅ Все тестовые данные успешно добавлены!")


if __name__ == "__main__":
    try:
        asyncio.run(seed_data())
    except KeyboardInterrupt:
        print("\n⚠️  Операция прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Ошибка при заполнении данных: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)