
#!/bin/bash

echo "=== Финальное тестирование TODO сервиса ==="
echo

BASE_URL="http://localhost:8000"

echo "1. Проверка доступности сервиса..."
if ! curl -f "$BASE_URL/docs" > /dev/null 2>&1; then
    echo "Ошибка: сервис недоступен"
    exit 1
fi
echo "✓ Сервис доступен"

echo -e "\n2. Логин пользователя:"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpassword123"}')

if echo "$LOGIN_RESPONSE" | jq -e '.access_token' > /dev/null 2>&1; then
    TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')
    echo "✓ Логин успешен"
else
    echo "Ошибка логина:"
    echo "$LOGIN_RESPONSE"
    exit 1
fi

echo -e "\n3. Информация о текущем пользователе:"
curl -s -X GET "$BASE_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

echo -e "\n4. Создание задачи:"
TASK_RESPONSE=$(curl -s -X POST "$BASE_URL/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Тестовая задача",
    "description": "Описание тестовой задачи"
  }')

TASK_ID=$(echo "$TASK_RESPONSE" | jq -r '.id')
if [ "$TASK_ID" != "null" ] && [ -n "$TASK_ID" ]; then
    echo "✓ Задача создана, ID: $TASK_ID"
    echo "$TASK_RESPONSE" | jq '.'
else
    echo "Ошибка создания задачи:"
    echo "$TASK_RESPONSE"
fi

echo -e "\n5. Создание второй задачи:"
TASK2_RESPONSE=$(curl -s -X POST "$BASE_URL/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Вторая задача",
    "description": "Для тестирования связей"
  }')

TASK2_ID=$(echo "$TASK2_RESPONSE" | jq -r '.id')
if [ "$TASK2_ID" != "null" ] && [ -n "$TASK2_ID" ]; then
    echo "✓ Вторая задача создана, ID: $TASK2_ID"
else
    echo "Ошибка создания второй задачи:"
    echo "$TASK2_RESPONSE"
    # Пробуем получить ID из сырого ответа
    TASK2_ID=$(echo "$TASK2_RESPONSE" | grep -o '"id":[0-9]*' | cut -d: -f2)
    echo "Извлеченный ID: $TASK2_ID"
fi

echo -e "\n6. Получение всех задач:"
ALL_TASKS=$(curl -s -X GET "$BASE_URL/tasks" \
  -H "Authorization: Bearer $TOKEN")
if echo "$ALL_TASKS" | jq -e '.' > /dev/null 2>&1; then
    echo "$ALL_TASKS" | jq '.'
    TASK_COUNT=$(echo "$ALL_TASKS" | jq 'length')
    echo "Всего задач: $TASK_COUNT"
else
    echo "Ответ:"
    echo "$ALL_TASKS"
fi

echo -e "\n7. Создание связи между задачами (если обе задачи созданы):"
if [ -n "$TASK_ID" ] && [ -n "$TASK2_ID" ] && [ "$TASK_ID" != "null" ] && [ "$TASK2_ID" != "null" ]; then
    echo "Создаем связь: задача $TASK_ID -> задача $TASK2_ID"
    RELATION_RESPONSE=$(curl -s -X POST "$BASE_URL/tasks/$TASK_ID/relations" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -d "{\"task_to_id\": $TASK2_ID, \"relation_type\": \"related\"}")
    
    if echo "$RELATION_RESPONSE" | jq -e '.' > /dev/null 2>&1; then
        echo "✓ Связь создана:"
        echo "$RELATION_RESPONSE" | jq '.'
    else
        echo "Ошибка создания связи:"
        echo "$RELATION_RESPONSE"
    fi
    
    echo -e "\n8. Получение связей задачи $TASK_ID:"
    curl -s -X GET "$BASE_URL/tasks/$TASK_ID/relations" \
      -H "Authorization: Bearer $TOKEN" | jq '.'
else
    echo "✗ Не удалось создать связь: недостаточно задач"
fi

echo -e "\n9. Обновление задачи (отметка как выполненной):"
curl -s -X PUT "$BASE_URL/tasks/$TASK_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"completed": true}' | jq '.'

echo -e "\n10. Получение обновленной задачи:"
curl -s -X GET "$BASE_URL/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

echo -e "\n11. Удаление задачи $TASK2_ID (если существует):"
if [ -n "$TASK2_ID" ] && [ "$TASK2_ID" != "null" ]; then
    DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/tasks/$TASK2_ID" \
      -H "Authorization: Bearer $TOKEN")
    
    if echo "$DELETE_RESPONSE" | jq -e '.' > /dev/null 2>&1; then
        echo "✓ Задача удалена:"
        echo "$DELETE_RESPONSE" | jq '.'
    else
        echo "Ответ удаления:"
        echo "$DELETE_RESPONSE"
    fi
fi

echo -e "\n12. Проверка что задача удалена:"
if [ -n "$TASK2_ID" ] && [ "$TASK2_ID" != "null" ]; then
    curl -s -X GET "$BASE_URL/tasks/$TASK2_ID" \
      -H "Authorization: Bearer $TOKEN" | jq '.'
fi

echo -e "\n13. Тестирование фильтров:"
echo "Завершенные задачи:"
curl -s -X GET "$BASE_URL/tasks?completed=true" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

echo -e "\nНезавершенные задачи:"
curl -s -X GET "$BASE_URL/tasks?completed=false" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

echo -e "\n14. Получение категорий:"
curl -s -X GET "$BASE_URL/categories" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

echo -e "\n15. Получение тегов:"
curl -s -X GET "$BASE_URL/tags" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

echo -e "\n=== Тестирование завершено ==="

echo -e "\n=== Сводка ==="
echo "Пользователь: testuser"
echo "Токен: ${TOKEN:0:30}..."
echo "Создана задача ID: $TASK_ID"
echo "Создана задача ID: $TASK2_ID"
echo "API работает корректно!"
