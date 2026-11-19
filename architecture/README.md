# Архитектура ИС ОСАГО — Diagrams-as-Code (C4 Model, Lab 5)

Вся архитектура описана кодом PlantUML. CI (GitHub Actions, `.github/workflows/render-docs.yml`) при каждом push и Pull Request в `main`:
1. проверяет стандарты кодирования и глоссарий ID (`scripts/check_rules.py`);
2. валидирует синтаксис PlantUML и рендерит PNG + SVG в `docs/images/` (`scripts/render.sh`);
3. собирает интерактивную карту `docs/index.html`;
4. при ошибке сборка падает с ❌, при push в `main` бот коммитит артефакты.

## Структура

```
architecture/
├── src/
│   ├── core/                  # ТИМЛИД: обёртки C4 + единые стили (skinparam/теги ТОЛЬКО здесь)
│   │   ├── C4_Context|Container|Component|Dynamic|Deployment.puml
│   │   ├── styles.puml  class_style.puml  deployment_style.puml
│   ├── main.puml              # ТИМЛИД: сводная диаграмма контейнеров (L2)
│   ├── team_tagan/            # ТИМЛИД: глобальные L0, L1, L2 (личная), динамика, развёртывание
│   ├── kiselev_api/           # Киселев Д.А.: API — L0, L1, L2, L3, L4, dynamic, deployment
│   ├── uskov_worker/          # Усков М.В.: Worker
│   ├── mekhova_backoffice/    # Мехова А.С.: Backoffice
│   └── romanov_webapp/        # Романов Н.И.: Web App
├── glossary/                  # глоссарий глобальных ID (csv + md)
├── scripts/                   # check_rules.py, render.sh, build_index.py
└── docs/                      # ГЕНЕРИРУЕТСЯ CI: images/**.png|svg, index.html, логи
```

Каждый разработчик меняет только свою папку — конфликтов слияния нет (модульный принцип).

## Стандарты (раздел 4.4 методички)

| Код | Правило |
|---|---|
| R1 | Только `Rel(от, кому, "описание", "протокол")`. Запрещены `Rel_D/R/L/U`, `Lay_*`, `-[hidden]-` |
| R2 | Никаких `skinparam`, `Add*Tag`, `Update*Style`, цветов `#RRGGBB` — только `$tags="ext|target|city|staff|outsider|changed|async|rbac|audit"` из core |
| R3 | У каждой стрелки — описание бизнес-действия и технический протокол (`HTTPS/JSON`, `SQL/TCP 5432` …) |
| R4 | Обе стороны связи объявлены в файле (опечатка в ID = ошибка) |
| R5 | Персоны, системы, контейнеры и границы — только ID из `glossary/glossary_ids.csv` |
| R6 | Стыковочные компоненты API: `auth_comp`, `access_comp`, `policy_comp`, `payment_comp`, `accident_comp`, `inspection_comp`, `admin_comp`, `audit_comp`, `task_queue_comp` |
| R7 | Единственный `!include` — `../core/C4_*.puml` (без URL) |

Разрешены глобальные `LAYOUT_TOP_DOWN()/LAYOUT_LEFT_RIGHT()` и `SHOW_LEGEND()` — они не позиционируют отдельные связи.

## Локальная проверка

```bash
cd architecture
python3 scripts/check_rules.py                 # стандарты и глоссарий
bash scripts/render.sh /путь/к/plantuml.jar    # синтаксис + PNG/SVG (нужны Java 11+ и Graphviz)
python3 scripts/build_index.py                 # карта docs/index.html
```

Предпросмотр в VS Code: расширение **PlantUML** (jebbs) + локальный сервер
`docker compose -f architecture/docker-compose.plantuml.yml up -d` → в настройках `plantuml.render = PlantUMLServer`, `plantuml.server = http://localhost:8080`.
Если сервер не подтягивает `../core/*.puml`, переключите `plantuml.render` на `Local` (нужна Java).

## Процесс (Git Flow)

1. Тимлид: ветка `lab5/devops-setup` → PR → merge; включает Branch Protection для `main`.
2. Разработчик: ветка `feature/<фамилия>-c4` от свежего `main`, коммиты только в свою папку → PR в `main`.
3. CI ❌ → разработчик читает лог в Actions, исправляет, пушит снова до ✅.
4. Тимлид оставляет комментарии ревью в коде, после исправлений — Approve и Merge.

## Промпты LLM и журнал применения (гл. 6 курсовой)

`prompts/` — версионируемые промпты: `system_c4_architect.md` (System Prompt), `fewshot_rel.md` (Few-Shot),
`cot_dynamic.md` (Chain-of-Thought). После применения LLM автор фиксирует результат:

```bash
python3 scripts/llm_log.py --prompt prompts/system_c4_architect.md --model "<модель>" \
    --author <логин> --files src/<папка>/<файл>.puml --decision accepted|edited|rejected
```

Запись (паттерн, версия промпта, хэши файлов, результат check_rules) добавляется в `docs/llm_log.jsonl`.
Персональные данные и тексты ответов модели в журнал не пишутся.
