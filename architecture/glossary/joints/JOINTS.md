# Реестр стыков

> Сгенерирован из `joints.json`. Стык — связь между компонентами РАЗНЫХ контейнеров.

| № | Тип | От | К | Статус | Контракты / endpoints | Примечание |
|---|---|---|---|---|---|---|
| J-01 | http | `webapp.AuthApiClient` | `api.AuthController` | ok | POST /api/auth/code, POST /api/auth/verify |  |
| J-02 | http | `webapp.AccidentApiClient` | `api.AccidentController` | ok | POST /api/claims, GET /api/claims, GET /api/claims/{claim_id}, POST /api/claims/{claim_id}/assign, POST /api/claims/{claim_id}/status |  |
| J-03 | http | `webapp.InspectionApiClient` | `api.InspectionController` | mismatch | POST /api/claims/{claim_id}/inspection, POST /api/claims/{claim_id}/photos, POST /api/claims/{claim_id}/signature, GET /api/claims/{claim_id}/protocol | Клиент Никиты (inspection_logic/integration/api_client.py) шлёт POST {base}/inspections с телом DamageAssessmentDTO — такого маршрута и такого тела в API нет. |
| J-04 | http | `webapp.PolicyApiClient` | `api.PaymentController` | partial | POST /api/payments/session | Только оплата. Расчёт, оформление и PDF полиса из описания PolicyApiClient принимающего контроллера не имеют. |
| J-05 | http | `backoffice.AuthApiClient` | `api.AuthController` | ok | POST /api/auth/code, POST /api/auth/verify |  |
| J-06 | http | `backoffice.AdminApiClient` | `api.AdminController` | ok | GET /api/admin/users, POST /api/admin/users, GET /api/admin/tariffs, PUT /api/admin/tariffs |  |
| J-07 | http | `backoffice.OperationsApiClient` | `api.AdminController` | ok | POST /api/admin/tasks/{task_id}/restart, GET /api/admin/policies, GET /api/admin/payments | Перезапуск задач, поиск полисов и статусы платежей принимает AdminController (после правки L3). |
| J-08 | http | `backoffice.AuditApiClient` | `api.AdminController` | ok | GET /api/admin/audit |  |
| J-09 | queue | `api.TaskQueueFacade` | `worker.OutboxPoller` | ok | OutboxTask | API кладёт запись в outbox (через AccidentRepository), Worker забирает. Тип задачи — TaskType. |
| J-10 | store | `api.AccidentRepository` | `worker.AuditRepository` | ok | OutboxTask | Общая таблица очереди: API — писатель, Worker — читатель и обновляет статусы. |
| J-11 | store | `api.FileRepository` | `worker.FileRepository` | ok | StoredDocument | API кладёт фото и подписи, Worker читает их и сохраняет PDF. |
| J-12 | store | `api.TariffRepository` | `worker.TariffRepository` | ok | MarginReportDTO | API читает и меняет тарифы и отдаёт результаты маржи, Worker читает данные расчёта и пишет результаты маржи (MarginReportDTO). |
| J-13 | store | `api.AccidentRepository` | `worker.TransactionRepository` | ok | TransactionRecord | API пишет транзакции (AccidentRepository, PaymentService), Worker читает их и обновляет статусы (TransactionRepository). |
| J-14 | http | `backoffice.FinanceApiClient` | `api.AdminController` | ok | GET /api/admin/finance/margin, GET /api/admin/finance/payments, POST /api/admin/finance/invoices | Финансовые запросы принимает AdminController (после правки L3). |
