# Insurance-system
Insurance system pet project


pip install -r requirements.txt
uvicorn app.main:app --reload


app/
├── domain/          сущности, enum'ы, доменные ошибки
├── api/             контроллеры (FastAPI routers) + pydantic-схемы
├── services/        AccidentService, InspectionService, AuditService + интерфейсы
├── strategies/      AssignmentStrategy + Free/Region (паттерн Strategy)
├── integration/     TaskQueueFacade, AisOsagoFacade, генерация PDF
├── repositories/    AccidentRepository (SQLite), FileRepository (ФС) + интерфейсы
├── worker.py        имитация Worker (генерация PDF-протокола)
├── dependencies.py  композиционный корень (DI)
└── main.py          точка сборки
static/              демо-UI (index.html, style.css, app.js)
requirements.txt     fastapi, uvicorn, python-multipart


Что реализовано
Strategy — ?strategy=free|region на эндпоинте /assign, подмена в рантайме через DI
SOLID — контроллеры зависят от IAccidentService, сервисы — от IAccidentRepository/IFileRepository/ITaskQueue/IAisOsagoGateway, всё внедряется через __init__
Type hints — во всех сигнатурах (UUID, list[bytes], UUID | None, AccidentClaim…)
Полный цикл ДТП: регистрация → назначение эксперта → осмотр → фото → подпись → PDF-протокол

Что проверено
Регистрация (201), список (200), назначение region/free (200 — правильно подбирает эксперта)
Осмотр, загрузка фото, подпись, готовый PDF (%PDF-1.4, 1141 байт)
Неверный полис → 502 (АИС ОСАГО), неизвестное заявление → 404
Статический UI отдаётся, адаптивный (media query на 640px)