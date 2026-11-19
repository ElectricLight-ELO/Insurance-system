# Глоссарий компонентов ИС ОСАГО

> Файл сгенерирован из `glossary.json` (`python build_glossary.py`). Вручную не править.

Всего компонентов: **88**. API — 20, Worker — 23, Backoffice — 22, Web App — 23.

## API (FastAPI) — владелец: Дима

| Компонент | Слой | Технология | Описание | Статус |
|---|---|---|---|---|
| `AdminController` | Контроллеры | FastAPI Router | Пользователи, тарифы, аудит, задачи, полисы, финансовые отчеты | изменён на ревью |
| `AuthController` | Контроллеры | FastAPI Router | Вход по одноразовому коду | изменён на ревью |
| `InspectionController` | Контроллеры | FastAPI Router | Результаты осмотра, фото, подпись | базовый |
| `AccidentController` | Контроллеры | FastAPI Router | Заявления о ДТП, назначение эксперта | базовый |
| `PaymentController` | Контроллеры | FastAPI Router | Оплата, webhook | изменён на ревью |
| `AdminService` | Сервисы | Python | Учетные записи, тарифы, финансы, вопросы клиентам | изменён на ревью |
| `AccessService` | Сервисы | Python · Strategy | Выпуск токена и проверка прав (RBAC) | изменён на ревью |
| `AuditService` | Сервисы | Python | Запись событий аудита по каждому действию | базовый |
| `InspectionService` | Сервисы | Python | Акт осмотра, подпись, задача на PDF | базовый |
| `AccidentService` | Сервисы | Python | Заявление, проверка полиса, назначение | изменён на ревью |
| `PaymentService` | Сервисы | Python | Платежная сессия, обработка webhook | изменён на ревью |
| `TariffRepository` | Фасады и репозитории | SQLAlchemy | Тарифы, лог отчетов | изменён на ревью |
| `EmailFacade` | Фасады и репозитории | SMTP Client | Вопросы и корректировки | изменён на ревью |
| `UserRepository` | Фасады и репозитории | SQLAlchemy | Пользователи, роли, клиенты, полисы | изменён на ревью |
| `SmsGatewayFacade` | Фасады и репозитории | HTTP Client | Отправка кода | изменён на ревью |
| `AccidentRepository` | Фасады и репозитории | SQLAlchemy | Заявления, акты, транзакции, аудит и очередь | базовый |
| `FileRepository` | Фасады и репозитории | PyMongo | Фото, подписи, PDF | базовый |
| `TaskQueueFacade` | Фасады и репозитории | SQL Client | Задачи в очередь для Worker | базовый |
| `AisOsagoFacade` | Фасады и репозитории | HTTP Client | КБМ, ТС, водители, наличие полиса | базовый |
| `PaymentGatewayFacade` | Фасады и репозитории | HTTP Client | Сессии, отчеты о поступлениях | изменён на ревью |

## Worker (Python / Celery) — владелец: Миша

| Компонент | Слой | Технология | Описание | Статус |
|---|---|---|---|---|
| `OutboxPoller` | Прием задач | Celery Task | Забирает задачи из outbox | изменён на ревью |
| `Scheduler` | Прием задач | Celery Beat | Задачи по расписанию | изменён на ревью |
| `RegistrationTask` | Задачи | Celery Task | Регистрация договора, повторная проверка | изменён на ревью |
| `PdfTask` | Задачи | Celery Task | PDF полисов и протоколов | изменён на ревью |
| `FileCleanupTask` | Задачи | Celery Task | Удаление устаревших файлов | изменён на ревью |
| `NotificationTask` | Задачи | Celery Task | Письма: полисы, чеки, протоколы, сбои | изменён на ревью |
| `MarginCalculationTask` | Задачи | Celery Task | Расчет маржи | базовый |
| `ReportTask` | Задачи | Celery Task | Отчеты, счета и акты | изменён на ревью |
| `GatewayReconciliationTask` | Задачи | Celery Task | Сверка платежей | базовый |
| `ContractService` | Сервисы | Python | Регистрация договора в АИС после оплаты | изменён на ревью |
| `DocumentService` | Сервисы | Python | Сборка PDF, очистка файлов | изменён на ревью |
| `NotificationService` | Сервисы | Python | Шаблоны писем и вложения | изменён на ревью |
| `MarginService` | Сервисы | Python | Агрегация, расчет маржи и КВ | базовый |
| `ReportService` | Сервисы | Python | Отчеты по марже, счета и акты | изменён на ревью |
| `ReconciliationService` | Сервисы | Python | Сопоставление поступлений | базовый |
| `AuditService` | Сервисы | Python | Статусы задач и логи | базовый |
| `AisOsagoFacade` | Фасады и репозитории | HTTP Client | Регистрация договора, проверка полиса | изменён на ревью |
| `FileRepository` | Фасады и репозитории | PyMongo | Фото, подписи, PDF | изменён на ревью |
| `EmailFacade` | Фасады и репозитории | SMTP Client | Полисы, чеки, счета, отчеты, уведомления | изменён на ревью |
| `TariffRepository` | Фасады и репозитории | SQLAlchemy | Данные для расчета, результаты маржи | изменён на ревью |
| `TransactionRepository` | Фасады и репозитории | SQLAlchemy | Транзакции, платежи, КВ | изменён на ревью |
| `PaymentGatewayFacade` | Фасады и репозитории | HTTP Client | Статусы платежей | базовый |
| `AuditRepository` | Фасады и репозитории | SQLAlchemy | Outbox, статусы задач, аудит | базовый |

## Backoffice (React SPA) — владелец: Амелия

| Компонент | Слой | Технология | Описание | Статус |
|---|---|---|---|---|
| `AppRouter` | Маршруты | React Router | Защита страниц по роли: админ, поддержка, ИБ, бухгалтер | базовый |
| `LoginPage` | Страницы | React Page | Вход по одноразовому коду | базовый |
| `UsersRolesPage` | Страницы | React Page | Пользователи и роли | базовый |
| `TariffsPage` | Страницы | React Page | Тарифные сетки и коэффициенты | базовый |
| `TasksPage` | Страницы | React Page | Сбойные задачи, перезапуск | базовый |
| `PolicySearchPage` | Страницы | React Page | Поиск полисов, статусы платежей | базовый |
| `AuditLogPage` | Страницы | React Page | Журнал аудита, расследования | базовый |
| `FinanceDashboard` | Страницы | React Page | Маржа, оплаты, счета и акты | базовый |
| `AuthLogic` | Логика | React Context | Токен и роль пользователя | базовый |
| `AdminLogic` | Логика | React Hooks | Формы пользователей, ролей и тарифов | базовый |
| `DocumentViewer` | Логика | React Component | Просмотр PDF полисов, протоколов и актов | изменён на ревью |
| `OperationsLogic` | Логика | React Hooks | Задачи, поиск полисов, статусы | базовый |
| `ReportExporter` | Логика | SheetJS | Выгрузка отчетов и журнала в Excel / CSV | изменён на ревью |
| `AuditLogic` | Логика | React Hooks | Фильтры журнала, выгрузка | базовый |
| `FinanceLogic` | Логика | React Hooks | Дашборд маржи, счета и акты | базовый |
| `AuthApiClient` | API-клиенты | TypeScript | Запрос и проверка кода, токен | базовый |
| `AdminApiClient` | API-клиенты | TypeScript | Пользователи, роли, тарифы | базовый |
| `OperationsApiClient` | API-клиенты | TypeScript | Задачи, полисы, платежи | базовый |
| `AuditApiClient` | API-клиенты | TypeScript | Журнал аудита | базовый |
| `FinanceApiClient` | API-клиенты | TypeScript | Маржа, оплаты, счета и акты | базовый |
| `HttpClient` | HTTP | axios | Токен в каждом запросе, 401/403, повторы | базовый |
| `NotificationCenter` | HTTP | React Component | Уведомления об ошибках и результатах операций | изменён на ревью |

## Web App (React SPA) — владелец: Никита

| Компонент | Слой | Технология | Описание | Статус |
|---|---|---|---|---|
| `AppRouter` | Маршруты | React Router | Защита страниц по роли: гость, клиент, агент, менеджер, диспетчер, эксперт | изменён на ревью |
| `CalculatorPage` | Страницы | React Page | Расчет стоимости (в т.ч. для гостя) | изменён на ревью |
| `CheckoutPage` | Страницы | React Page | Оформление и оплата полиса | изменён на ревью |
| `CabinetPage` | Страницы | React Page | Личный кабинет, скачивание полиса | изменён на ревью |
| `AgentWorkplace` | Страницы | React Page | Оформление полисов и договоров агентом | изменён на ревью |
| `ManagerWorkplace` | Страницы | React Page | Отчеты, агенты, сложные случаи | изменён на ревью |
| `AccidentPage` | Страницы | React Page | Регистрация заявления о ДТП | базовый |
| `DispatcherPage` | Страницы | React Page | Заявление по звонку, назначение эксперта | изменён на ревью |
| `ExpertDashboard` | Страницы | React Page | Назначенные эксперту дела | базовый |
| `InspectionPage` | Страницы | React Page | Осмотр, фото, подписание акта | базовый |
| `AuthLogic` | Логика и UI | React Context | Токен и роль пользователя | базовый |
| `PolicyLogic` | Логика и UI | React Hooks | Расчет, оформление, полисы и отчеты | изменён на ревью |
| `FormWizard` | Логика и UI | React Component | Пошаговая форма ввода данных ДТП | базовый |
| `AccidentLogic` | Логика и UI | React Hooks | Черновик заявления, валидация полей | базовый |
| `PhotoUploader` | Логика и UI | React Component | Превью; проверка формата и размера | изменён на ревью |
| `ExpertCasesLogic` | Логика и UI | React Hooks | Список дел, фильтры, статусы | изменён на ревью |
| `InspectionLogic` | Логика и UI | React Hooks | Сбор результатов; оценка ущерба по категории | изменён на ревью |
| `SignaturePad` | Логика и UI | React Component | Канвас для электронной подписи | базовый |
| `AuthApiClient` | API-клиенты | TypeScript | Вход по коду, обновление токена | изменён на ревью |
| `PolicyApiClient` | API-клиенты | TypeScript | Расчет, оформление, оплата, PDF полиса | изменён на ревью |
| `AccidentApiClient` | API-клиенты | TypeScript | Заявления, статусы, назначение, дела | изменён на ревью |
| `InspectionApiClient` | API-клиенты | TypeScript | Фото, результаты, подпись | базовый |
| `HttpClient` | HTTP | axios | Токен в каждом запросе, 401/403, повторы | изменён на ревью |

## Одноимённые компоненты в разных контейнерах

| Имя | Где | Решение | Комментарий |
|---|---|---|---|
| `AuthLogic` | backoffice, webapp | same_role | Одна и та же логика хранения токена и роли; допускается общий пакет фронта. |
| `HttpClient` | backoffice, webapp | same_role | Один и тот же axios-клиент; допускается общий пакет фронта. |
| `AppRouter` | backoffice, webapp | different_role | Разные наборы маршрутов и ролей (Web App — клиент/агент/эксперт, Backoffice — админ/поддержка/финансы). |
| `AuthApiClient` | backoffice, webapp | different_role | Один и тот же endpoint входа по коду, но разные клиенты; тело запроса задаёт contracts.auth. |
| `AuditService` | api, worker | different_role | API пишет события аудита, Worker пишет статусы задач и логи. |
| `AisOsagoFacade` | api, worker | same_interface | API: КБМ, ТС, водители, полис. Worker: регистрация договора, повторная проверка. Нужен ОДИН интерфейс IAisOsagoGateway. |
| `EmailFacade` | api, worker | same_interface | API: вопросы и корректировки. Worker: полисы, чеки, отчёты. Нужен один интерфейс IEmailGateway. |
| `PaymentGatewayFacade` | api, worker | same_interface | API: создание сессии и отчёты о поступлениях. Worker: статусы платежей для сверки. Один интерфейс IPaymentGateway. |
| `FileRepository` | api, worker | same_interface | API пишет фото и подписи, Worker читает их и пишет PDF. Один интерфейс IFileRepository и одна схема документов DB_FILES. |
| `TariffRepository` | api, worker | same_interface | API читает и меняет тарифы, Worker читает данные для расчёта и пишет маржу. Одна схема DB_TARIFS. |
