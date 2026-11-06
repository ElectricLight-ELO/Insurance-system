# Insurance-system
Insurance system pet project
<img width="1862" height="893" alt="image" src="https://github.com/user-attachments/assets/61deace7-987f-474a-b498-6133c30a6005" />
<img width="1842" height="870" alt="image" src="https://github.com/user-attachments/assets/a48ab005-df9b-4947-82fd-b8f178c057a1" />
<img width="1699" height="891" alt="image" src="https://github.com/user-attachments/assets/5eeda4f4-5b16-4137-bcff-91c1045a69ed" />
<img width="1344" height="833" alt="image" src="https://github.com/user-attachments/assets/d934ab63-6e72-4726-aea1-cd3c832dfcdf" />
db photo-
<img width="1171" height="724" alt="image" src="https://github.com/user-attachments/assets/3826c191-9160-4295-aa85-c7ab528167ad" />


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
