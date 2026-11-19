## Что сделано
<!-- какие уровни C4 добавлены/изменены: L0, L1, L2, L3, L4, dynamic, deployment -->

## Чек-лист разработчика
- [ ] Файлы лежат только в своей папке `architecture/src/<фамилия_контейнер>/`
- [ ] Первая строка после `@startuml` — `!include ../core/C4_*.puml` (без URL)
- [ ] Только `Rel(...)` — без `Rel_D/R/L/U`, `Lay_*`, `-[hidden]-`
- [ ] Нет `skinparam`, `Add*Tag`, цветов `#RRGGBB` — только `$tags="..."` из core
- [ ] У каждой стрелки есть описание и протокол (HTTPS/JSON, SQL/TCP 5432 …)
- [ ] ID персон, систем и контейнеров — из `architecture/glossary/glossary_ids.csv`
- [ ] Локально прошли `python3 architecture/scripts/check_rules.py` и рендер в VS Code
- [ ] Сборка CI зелёная ✅

## Ревьюер
@mrW0LFHACK (тимлид)
