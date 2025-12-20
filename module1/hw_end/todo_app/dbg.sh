#!/bin/bash

echo "=== ДЕБАГ TODO сервиса ==="
BASE_URL="http://localhost:8000"

echo "1. Проверка /docs:"
curl -s "$BASE_URL/docs" | head -20

echo -e "\n\n2. Регистрация нового пользователя (RAW вывод):"
curl -v -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "debuguser@test.com",
    "username": "debuguser",
    "password": "debugpass123"
  }' 2>&1 | grep -A5 -B5 "HTTP\|{"

echo -e "\n\n3. Логин (RAW вывод):"
curl -v -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "debuguser",
    "password": "debugpass123"
  }' 2>&1 | grep -A5 -B5 "HTTP\|{"

echo -e "\n\n4. Простой GET запрос без авторизации:"
curl -v "$BASE_URL/tasks" 2>&1 | head -20

echo -e "\n\n=== ДЕБАГ завершен ==="