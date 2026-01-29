#!/bin/bash
echo "🧪 Запуск полного тестового сценария..."

# 1. Проверка здоровья
echo -e "\n1️⃣  Health check:"
curl -s http://localhost:8000/health | jq .

# 2. Добавление товара в заказ
echo -e "\n2️⃣  Добавление товара в заказ:"
curl -s -X POST "http://localhost:8000/api/v1/orders/1/items" \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "item_id": 1, "quantity": 2}' | jq .

# 3. Проверка заказа
echo -e "\n3️⃣  Проверка заказа:"
curl -s "http://localhost:8000/api/v1/orders/1" | jq .

# 4. Проверка остатков
echo -e "\n4️⃣  Проверка остатков товара:"
curl -s "http://localhost:8000/api/v1/items/1" | jq .

# 5. Повторное добавление
echo -e "\n5️⃣  Повторное добавление того же товара:"
curl -s -X POST "http://localhost:8000/api/v1/orders/1/items" \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "item_id": 1, "quantity": 3}' | jq .

# 6. Проверка итогового состояния
echo -e "\n6️⃣  Итоговое состояние заказа:"
curl -s "http://localhost:8000/api/v1/orders/1" | jq .

echo -e "\n7️⃣  Итоговые остатки:"
curl -s "http://localhost:8000/api/v1/items/1" | jq .

echo -e "\n✅ Тестовый сценарий завершён!"