# FastAPI Microservices Project

Два микросервиса на FastAPI: TODO-сервис и URL Shortener.
Ссылки на докерхаб:
https://hub.docker.com/r/zhmikh/todo-service
https://hub.docker.com/r/zhmikh/shorturl-service

Собрано для мака. Может давать ошибку при запуске на винде или линуксе. 

### Как поднять?
```bash
# Клонирование репозитория
git clone https://github.com/Zhmikhail/HSE_Yurkov_Mikhail_seminar_nastaynika
cd hw_end

# Запуск всех сервисов
docker-compose up -d

# Остановка сервисов
docker-compose down

# Остановка с удалением томов данных
docker-compose down -v
```

По каждому сервису есть автодока в сваггере

http://localhost:8001/docs
http://localhost:8000/docs

## Сервисы

### 1. TODO-сервис
**ВЕРХОУРОВНЕВОЕ ОПИСАНИЕ**
Я практически не менял архитектуру, которая первой приходит в голову. Просто добавил немного функционала (теги, задачи, категории). Теперь задачам можно присуждать теги, объединять в категории, делать подзадачи. Ничего интересного, только расширение функционала. Если у вас ограниченное время, я бы предложил запустить файл теста (test.sh) который за вас прогонит и круд, и мой функционал, и перейти к следующему сервису - на него я уделил больше времени.

**ТЕХНИЧЕСКИЕ ПОДРОБНОСТИ**
Если вы хотите только проверить работоспособность сервиса, можно запустить 

```bash
bash todo_app/test.sh
```
В данном скрипте происходит тест всех ручек приложения с выводом, по которому можно понять что вообще произошло.
Если вы хотите самостоятельно "потыкать", вот запросы:



```bash
# =====================Работа юзера========================
# 1. Регистрация юзера
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "demo_user",
    "password": "SecurePass123!"
  }'
# 2. Вход и получение токена
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo_user",
    "password": "SecurePass123!"
  }')

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo "Токен: $TOKEN"

# 3. Создание категории
curl -X POST "http://localhost:8000/categories" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Работа",
    "color": "#FF6B6B"
  }'


#'

# 4. Создание тега
curl -X POST "http://localhost:8000/tags" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "важно",
    "color": "#4ECDC4"
  }'

#'
# 5. Создание задачи

curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Завершить проект",
    "description": "Финальная стадия разработки",
    "priority": 5,
    "due_date": "2024-12-31T23:59:59Z",
    "category_id": 1,
    "tag_ids": [1]
  }'

#'
# 5. Получение задач
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/tasks"

# =====================Работа с задачами========================

# 1. Только завершенные задачи
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/tasks?completed=true"

# 2. Задачи определенной категории
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/tasks?category_id=1"

# 3. Задачи с высоким приоритетом
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/tasks?priority=5"

# 4. Комбинированная фильтрация
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/tasks?completed=false&priority=4"

# 5. Отметка как выполненной
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"completed": true}'

# 6. Изменение приоритета и описания
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"priority": 3, "description": "Обновленное описание"}'

# 7. Удаление задачи
curl -X DELETE "http://localhost:8000/tasks/1" \
  -H "Authorization: Bearer $TOKEN"
```



### 2. URL Shortener

**ВЕРХОУРОВНЕВОЕ ОПИСАНИЕ**
На данный сервис ушло больше времени, так как я поставил еще одну задачу - генерация именно КРАТЧАЙШЕЙ ссылки. Я видел, что сервис от Яндекса генерит ссылки в 6 символов. Но можно ли короче? Я узнал, какие символы могут быть в качестве ссылки (из незарезервированных на веб символов в ASCII - это английский алфавит большими и маленькими буквами, цифры и символы -_~.). Таким образом, мы имеем алфавит из (26 + 26 + 10 + 4) 66 букв. Тогда имеем такие количества кодируемых слов в зависимости от количества символов:

1 - 66¹ = 66 комбинаций
2 - 66² = 4,356 комбинаций
3 - 66³ = 287,496 комбинаций  
4 - 66⁴ = 18,974,736 комбинаций

1. Я решил, что в качестве бизнес-применения данного разбиения можно сделать разделение на классы пользователей. Но как реально использовать эти возможности, может решить сам бизнес (я больше решал разработческую задачу, занимался пришиванием рукавов куда попало). Смысл в том, что я решил задачу генерации разных длин ссылок (вплоть до одного символа)
2. Добавил время жизни ссылки (в минутах, для более прозрачного тестирования). В проде, конечно, оно будет, как угодно.
3. Доработал статистику переходов. Теперь отправивший ссылку человек может узнать, сколько раз перешли по его ссылке.
4. Добавил ручки для админа, он сможет увидеть, что происходит в БД. 
5. Реализовал крон-питонфайлик, который чистит протухшие записи в БД. Запускается в докерфайле раз в 30 секунд для того, чтобы сожно было протестировать. В проде можно настроить раз в сутки. 

Разумеется, я не решил все вопросы данной предметной области. Например, при переполнении количества комбинаций следующая комбинация не сгенерируется (есть проверка на недублируемость ссылок, она не даст дублировать). Полагаю, если подумать, такого можно придумать много. 

**ТЕХНИЧЕСКИЕ ПОДРОБНОСТИ**

**1. Дифференциация по типам пользователей:**
- **Царь (tsar)**: 1 символ - для эксклюзивных ссылок
- **Премиум (premium)**: 2 символа - для VIP-клиентов
- **Стандарт (standard)**: 3 символа - для обычных пользователей
- **Бесплатный (free)**: 4 символа - для массового использования

**2. Алгоритм генерации:**
- Алфавит: 66 символов (`0-9a-zA-Z-_.~`)
- Случайная генерация с проверкой уникальности
- Автоматическое увеличение длины при коллизиях

**3. TTL (Time-To-Live):**
- Настраиваемое время жизни ссылок
- Автоматическая очистка протухших ссылок
- По умолчанию: 24 часа

**API Эндпоинты:**
- `POST /shorten` - Создание короткой ссылки
- `GET /{short_id}` - Перенаправление по короткой ссылке
- `GET /stats/{short_id}` - Статистика по ссылке

**Админские эндпоинты:**
- `GET /admin/urls` - Все ссылки в БД
- `GET /admin/urls/count` - Количество ссылок
- `GET /admin/urls/stats` - Статистика по типам пользователей

## 🐳 Запуск через Docker

### Предварительные требования
- Docker и Docker Compose
- Порты 8000 и 8001 свободны


### Как тестировать?
```bash
# =====================Разные юзеры========================
# 1. Бесплатный пользователь (4 символа, 24 часа)
curl -X POST "http://localhost:8001/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://free-user-example.com", "user_tier": "free"}'

# 2. Стандартный пользователь (3 символа)
curl -X POST "http://localhost:8001/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://standard-user-example.com", "user_tier": "standard"}'

# 3. Премиум пользователь (2 символа)
curl -X POST "http://localhost:8001/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://premium-user-example.com", "user_tier": "premium"}'

# 4. Царь (1 символ)
curl -X POST "http://localhost:8001/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://tsar-example.com", "user_tier": "tsar"}'

# ======================Проверка TTL=======================
# 1. Ссылка на 1 минуту (для быстрой проверки)
curl -X POST "http://localhost:8001/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://ttl-test.com", "ttl_minutes": 1, "user_tier": "free"}'

# 2. Проверить создание
curl "http://localhost:8001/stats/{short_id_from_previous_response}"

# 3. Подождать 1+ минуту и проверить снова (должна быть 410 ошибка)
curl "http://localhost:8001/{short_id}"

# ======================Статистика=======================

# Взять сымволы руски из сгенерированной сслыки
# 1. Проверить редирект (должен вернуть 302)
curl -v "http://localhost:8001/$short_id" 2>&1 | grep -E "(Location:|HTTP/)"

# 2. Проверить статистику (clicks должно быть 1)
curl "http://localhost:8001/stats/$short_id" | jq '.clicks'

# 3. Еще раз перейти по ссылке
curl -v "http://localhost:8001/$short_id" 2>&1 | grep -E "(Location:|HTTP/)"

# 4. Проверить статистику
curl "http://localhost:8001/stats/$short_id" | jq '.clicks'

# ======================Админское=======================
# 1. Все ссылки в системе
curl "http://localhost:8001/admin/urls" | jq '.'

# 2. Общее количество ссылок
curl "http://localhost:8001/admin/urls/count"

# 3. Статистика по тарифам (сколько пользователей каждого типа)
curl "http://localhost:8001/admin/urls/stats" | jq '.'

# 4. Проверить распределение по длинам ссылок
curl "http://localhost:8001/admin/urls" | jq '.[] | {short_id: .short_id, length: (.short_id | length)}'

```