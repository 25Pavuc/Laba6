# LABA 6 MADE BY FEDOSEEV PAVEL

# 1. Предметная область

Фармацевтическая компания

# 2. Функционал API

# Реализованные операции

GET (один ресурс) - Получение данных об одном объекте
GET (группа с фильтрами) - Получение списка с фильтрацией по параметрам 
POST (один ресурс) - Создание одного объекта 
POST (группа ресурсов) - Массовое создание нескольких объектов 
PATCH (один ресурс) - Частичное обновление одного объекта 
PATCH (группа ресурсов) - Массовое частичное обновление 
DELETE (один ресурс) - Удаление одного объекта 
DELETE (группа ресурсов) - Массовое удаление через параметр 

# 3. Эндпоинты API

# Производители (`/api/v1/manufacturers/`)

GET `/manufacturers/`- Список всех производителей 
GET  `/manufacturers/?name=Россия` - Фильтрация по названию 
GET  `/manufacturers/?country=Россия` -  Фильтрация по стране 
GET  `/manufacturers/1/` - Получить производителя с id=1 
POST  `/manufacturers/` - Создать одного производителя 
POST  `/manufacturers/`- Массовое создание (передать массив) 
PUT  `/manufacturers/1/` - Полное обновление производителя 
PATCH  `/manufacturers/1/` -  Частичное обновление 
PATCH  `/manufacturers/` - Массовое частичное обновление 
DELETE  `/manufacturers/1/` -  Удалить производителя 
DELETE `/manufacturers/?ids=1,2,3` -  Массовое удаление 

# Лекарства (`/api/v1/medicines/`)


GET `/medicines/` - Список всех лекарств 
GET  `/medicines/name=Парацетамол` - Фильтр по названию 
GET  `/medicines/manufacturer_id=1` - Фильтр по производителю 
GET  `/medicines/category=prescription` - Фильтр по категории 
GET  `/medicines/low_stock/` -  Лекарства с запасом < 10 
GET  `/medicines/1/` - Получить лекарство с id=1 
POST  `/medicines/` - Создать одно лекарство 
POST  `/medicines/` - Массовое создание 
PUT `/medicines/1/` - Полное обновление 
PATCH  `/medicines/1/` - Частичное обновление 
PATCH  `/medicines/` - Массовое частичное обновление 
DELETE  `/medicines/1/` - Удалить лекарство 
DELETE `/medicines/ids=1,2,3` - Массовое удаление 

# Заказы (`/api/v1/orders/`)


GET - `/orders/` - Список всех заказов 
GET - `/orders/tatus=pending` - Фильтр по статусу 
GET - `/orders/medicine_id=1` - Фильтр по лекарству 
GET - `/orders/1/` - Получить заказ с id=1 
POST - `/orders/` - Создать один заказ 
POST - `/orders/` - Массовое создание 
PUT - `/orders/1/` - Полное обновление 
PATCH - `/orders/1/` - Частичное обновление 
PATCH - `/orders/` - Массовое частичное обновление 
DELETE -  `/orders/1/` - Удалить заказ 
DELETE - `/orders/ids=1,2,3` - Массовое удаление 

# 4. Документация API

Документация автоматически сгенерирована с помощью Swagger/OpenAPI.

# Доступ к документации


Swagger UI (интерактивная) `http://127.0.0.1:8000/api/docs/` 
OpenAPI схема (JSON) `http://127.0.0.1:8000/api/schema/` 

# Примеры запросов

# GET с фильтрацией
```bash
# Получить всех производителей из России
curl -X GET "http://127.0.0.1:8000/api/v1/manufacturers/?country=Россия"

# Получить все рецептурные лекарства
curl -X GET "http://127.0.0.1:8000/api/v1/medicines/?category=prescription"