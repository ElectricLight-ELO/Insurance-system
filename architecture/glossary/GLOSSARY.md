# Глоссарий глобальных ID — ИС ОСАГО

Единый источник: `glossary_ids.csv` (его читает `scripts/check_rules.py`). Новый ID добавляет только тимлид через PR.

Правила: персоны, системы, контейнеры и границы на уровнях L0–L3 используют **только** эти ID. Компоненты внутри своего контейнера разработчик называет свободно, кроме стыковочных компонентов API (помечены `Component*`) — к ним подключаются другие контейнеры, поэтому их ID фиксированы.

| ID | Тип | Наименование | Владелец | Уровни |
|---|---|---|---|---|
| `guest` | Person | Гость (неавторизованный посетитель) | Таган А.М. | L0-L2 |
| `client` | Person | Клиент (страхователь / участник ДТП) | Таган А.М. | L0-L2 |
| `payer` | Person | Застрахованный клиент (плательщик) | Таган А.М. | L0-L2 |
| `agent` | Person | Страховой агент | Таган А.М. | L0-L2 |
| `manager` | Person | Менеджер отдела продаж | Таган А.М. | L0-L2 |
| `dispatcher` | Person | Диспетчер колл-центра | Таган А.М. | L0-L2 |
| `expert` | Person | Аварийный эксперт | Таган А.М. | L0-L2 |
| `support` | Person | Оператор поддержки | Таган А.М. | L0-L2 |
| `auditor` | Person | Сотрудник ИБ / аудитор | Таган А.М. | L0-L2 |
| `accountant` | Person | Бухгалтер | Таган А.М. | L0-L2 |
| `admin` | Person | Администратор | Таган А.М. | L0-L2 |
| `citizen` | Person | Граждане и клиенты (агрегат на L0) | Таган А.М. | L0 |
| `front_staff` | Person | Сотрудники фронт-офиса (агрегат на L0) | Таган А.М. | L0 |
| `back_staff` | Person | Сотрудники бэк-офиса (агрегат на L0) | Таган А.М. | L0 |
| `osago` | System | ИС ОСАГО (система целиком, чёрный ящик) | Таган А.М. | L0-L1 |
| `osago_service` | System_Boundary | Граница ИС ОСАГО на диаграмме контейнеров | Таган А.М. | L2 |
| `osago_core` | System | Остальная часть ИС ОСАГО на локальном L0 разработчика | Таган А.М. | L0 |
| `enterprise` | Enterprise_Boundary | Корпоративная ИТ-инфраструктура страховой компании | Таган А.М. | L0 |
| `city` | Boundary | Экосистема Smart City | Таган А.М. | L0 |
| `iam` | System | Служба авторизации (IAM) | Таган А.М. | L0 |
| `crm` | System | CRM страховой компании | Таган А.М. | L0 |
| `city_portal` | System_Ext | Городской портал услуг | Таган А.М. | L0 |
| `esia` | System_Ext | ЕСИА (Госуслуги) | Таган А.М. | L0 |
| `sitc` | System_Ext | Ситуационный центр / Система-112 | Таган А.М. | L0 |
| `soc` | System_Ext | Городской центр мониторинга ИБ (SOC) | Таган А.М. | L0 |
| `ais_osago` | System_Ext | АИС ОСАГО (РСА) | Таган А.М. | L0-L3 |
| `payment_sys` | System_Ext | Платёжная система / эквайринг | Таган А.М. | L0-L3 |
| `sms_sys` | System_Ext | SMS-шлюз | Таган А.М. | L0-L3 |
| `email_sys` | System_Ext | E-mail система | Таган А.М. | L0-L3 |
| `mod_accident` | System | Модуль фиксации ДТП и осмотра (локальный L0) | Киселев Д.А. | L0 |
| `mod_finance` | System | Модуль финансового контроля и маржи (локальный L0) | Усков М.В. | L0 |
| `mod_backoffice` | System | Модуль администрирования и аудита (локальный L0) | Мехова А.С. | L0 |
| `mod_sales` | System | Модуль продажи и оформления полисов (локальный L0) | Романов Н.И. | L0 |
| `api` | Container | API (FastAPI) | Киселев Д.А. | L2-L3 |
| `worker` | Container | Worker (Python / Celery) | Усков М.В. | L2-L3 |
| `backoffice` | Container | Backoffice (React SPA) | Мехова А.С. | L2-L3 |
| `web_app` | Container | Web App (React SPA) | Романов Н.И. | L2-L3 |
| `db_users` | ContainerDb | DB_USERS (PostgreSQL) | Киселев Д.А. | L2-L3 |
| `db_tarifs` | ContainerDb | DB_TARIFS (PostgreSQL) | Усков М.В. | L2-L3 |
| `db_audit` | ContainerDb | DB_AUDIT (PostgreSQL, outbox) | Киселев Д.А. | L2-L3 |
| `db_files` | ContainerDb | DB_FILES (MongoDB) | Киселев Д.А. | L2-L3 |
| `auth_comp` | Component* | AuthController — вход по одноразовому коду (стыковка Web App, Backoffice) | Киселев Д.А. | L3 |
| `access_comp` | Component* | AccessService — токены и RBAC (стыковка всех контроллеров) | Киселев Д.А. | L3 |
| `policy_comp` | Component* | PolicyController — расчёт и оформление полиса (стыковка Web App) | Киселев Д.А. | L3 |
| `payment_comp` | Component* | PaymentController — оплата и webhook (стыковка Web App, платёжной системы) | Киселев Д.А. | L3 |
| `accident_comp` | Component* | AccidentController — заявления о ДТП (стыковка Web App) | Киселев Д.А. | L3 |
| `inspection_comp` | Component* | InspectionController — осмотр, фото, подпись (стыковка Web App) | Киселев Д.А. | L3 |
| `admin_comp` | Component* | AdminController — администрирование, аудит, финансы (стыковка Backoffice) | Киселев Д.А. | L3 |
| `audit_comp` | Component* | AuditService — журнал аудита | Киселев Д.А. | L3 |
| `task_queue_comp` | Component* | TaskQueueFacade — очередь outbox (стыковка Worker) | Киселев Д.А. | L3 |
