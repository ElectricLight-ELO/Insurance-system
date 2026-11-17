# ИС ОСАГО — все диаграммы проекта

Папка собрана как репозиторий: каждая группа диаграмм в своей папке, внутри `puml/` (исходники PlantUML), `drawio/` (где есть) и `png/` (картинки).

| Папка | Что внутри |
|---|---|
| `01_Курсовая_гл2_IDEF0_UseCase_Activity` | Глава 2 курсовой: IDEF0 «как есть» и «как должно быть» (A-0, A0, A3), Use-Case (6 шт.), Activity. Номер в имени = номер рисунка |
| `02_L1_L2_контекст_и_контейнеры` | `итоговые/` — context и container; `по_участникам/` — личные контейнерные диаграммы Артема, Амелии, Димы, Миши, Никиты (ветка new era) |
| `03_L3_компоненты` | `итоговые/` — 4 диаграммы компонентов после ревью (API, Worker, Backoffice, Web App); `исходные_до_ревью/` — как было у участников |
| `04_L4_код` | 4 диаграммы классов (единый жёлтый цвет), puml + draw.io + png |
| `05_Lab0_ландшафт_динамика_развертывание` | Лабораторная 0: системный ландшафт, динамика (36 шагов), развёртывание всей системы |
| `06_Лаб4_команда` | Лабораторная 4 по участникам: Мехова, Романов, Таган (тимлид: глобальные ландшафт, динамика, развёртывание) — puml + png; Киселев и Усков — png из их отчётов (исходников puml у нас нет) |
| `07_Курсовая_гл4_ER_последовательности_UI_КТС` | Глава 4 курсовой: модель данных ERA, 3 диаграммы последовательностей, 6 макетов экранов, схема КТС |

## Как открыть
- `.puml` — plantuml.com, расширение PlantUML в VS Code или `java -jar plantuml.jar файл.puml`. Файлы Lab 0 и L1/L2 подключают C4 по ссылке из интернета; без интернета замените строку `!include https://…/C4_X.puml` на `!include <C4/C4_X>`.
- `.drawio` — app.diagrams.net → Файл → Открыть.
- В `06_Лаб4_команда` рядом с puml лежит `common.inc` — общие цвета и теги, его нужно держать в той же папке.

## Полный список файлов

- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.10_IDEF0_TO-BE_A3.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.11_UseCase_TO-BE_продажа_и_оформление.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.12_UseCase_TO-BE_урегулирование_ДТП.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.13_UseCase_TO-BE_финансы_поддержка_администрирование.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.1_IDEF0_AS-IS_A-0.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.2_IDEF0_AS-IS_A0.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.3_IDEF0_AS-IS_A3.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.4_UseCase_AS-IS_продажа_и_оформление.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.5_UseCase_AS-IS_урегулирование_ДТП.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.6_UseCase_AS-IS_финансы_поддержка_администрирование.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.7_Activity_AS-IS_оформление_полиса.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.8_IDEF0_TO-BE_A-0.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/drawio/2.9_IDEF0_TO-BE_A0.drawio`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.10_IDEF0_TO-BE_A3.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.11_UseCase_TO-BE_продажа_и_оформление.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.12_UseCase_TO-BE_урегулирование_ДТП.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.13_UseCase_TO-BE_финансы_поддержка_администрирование.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.1_IDEF0_AS-IS_A-0.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.2_IDEF0_AS-IS_A0.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.3_IDEF0_AS-IS_A3.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.4_UseCase_AS-IS_продажа_и_оформление.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.5_UseCase_AS-IS_урегулирование_ДТП.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.6_UseCase_AS-IS_финансы_поддержка_администрирование.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.7_Activity_AS-IS_оформление_полиса.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.8_IDEF0_TO-BE_A-0.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/png/2.9_IDEF0_TO-BE_A0.png`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/puml/2.11_UseCase_TO-BE_продажа_и_оформление.puml`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/puml/2.12_UseCase_TO-BE_урегулирование_ДТП.puml`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/puml/2.13_UseCase_TO-BE_финансы_поддержка_администрирование.puml`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/puml/2.4_UseCase_AS-IS_продажа_и_оформление.puml`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/puml/2.5_UseCase_AS-IS_урегулирование_ДТП.puml`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/puml/2.6_UseCase_AS-IS_финансы_поддержка_администрирование.puml`
- `01_Курсовая_гл2_IDEF0_UseCase_Activity/puml/2.7_Activity_AS-IS_оформление_полиса.puml`
- `02_L1_L2_контекст_и_контейнеры/итоговые/container.png`
- `02_L1_L2_контекст_и_контейнеры/итоговые/container.puml`
- `02_L1_L2_контекст_и_контейнеры/итоговые/context.png`
- `02_L1_L2_контекст_и_контейнеры/итоговые/context.puml`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Amelia/container.png`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Amelia/container.puml`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Artem/container.png`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Artem/container.puml`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Dima/container.png`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Dima/container.puml`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Misha/class.png`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Misha/class.puml`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Misha/component.png`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Misha/component.puml`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Misha/container.png`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Misha/container.puml`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Nikita/container.png`
- `02_L1_L2_контекст_и_контейнеры/по_участникам/Nikita/container.puml`
- `03_L3_компоненты/исходные_до_ревью/api_Дима_исходная.png`
- `03_L3_компоненты/исходные_до_ревью/backoffice_Амелия_исходная.png`
- `03_L3_компоненты/исходные_до_ревью/webapp_Никита_исходная.png`
- `03_L3_компоненты/исходные_до_ревью/worker_Миша_исходная.png`
- `03_L3_компоненты/итоговые/drawio/api_component.drawio`
- `03_L3_компоненты/итоговые/drawio/backoffice_component.drawio`
- `03_L3_компоненты/итоговые/drawio/webapp_component.drawio`
- `03_L3_компоненты/итоговые/drawio/worker_component.drawio`
- `03_L3_компоненты/итоговые/png/api_component.png`
- `03_L3_компоненты/итоговые/png/backoffice_component.png`
- `03_L3_компоненты/итоговые/png/webapp_component.png`
- `03_L3_компоненты/итоговые/png/worker_component.png`
- `03_L3_компоненты/итоговые/puml/api_component.puml`
- `03_L3_компоненты/итоговые/puml/backoffice_component.puml`
- `03_L3_компоненты/итоговые/puml/webapp_component.puml`
- `03_L3_компоненты/итоговые/puml/worker_component.puml`
- `04_L4_код/drawio/api_class.drawio`
- `04_L4_код/drawio/backoffice_class.drawio`
- `04_L4_код/drawio/webapp_class.drawio`
- `04_L4_код/drawio/worker_class.drawio`
- `04_L4_код/png/api_class.png`
- `04_L4_код/png/backoffice_class.png`
- `04_L4_код/png/webapp_class.png`
- `04_L4_код/png/worker_class.png`
- `04_L4_код/puml/api_class.puml`
- `04_L4_код/puml/backoffice_class.puml`
- `04_L4_код/puml/webapp_class.puml`
- `04_L4_код/puml/worker_class.puml`
- `05_Lab0_ландшафт_динамика_развертывание/png/deployment.png`
- `05_Lab0_ландшафт_динамика_развертывание/png/dynamic.png`
- `05_Lab0_ландшафт_динамика_развертывание/png/l0_landscape.png`
- `05_Lab0_ландшафт_динамика_развертывание/puml/deployment.puml`
- `05_Lab0_ландшафт_динамика_развертывание/puml/dynamic.puml`
- `05_Lab0_ландшафт_динамика_развертывание/puml/l0_landscape.puml`
- `06_Лаб4_команда/Киселев_API_ДТП/png/deployment.png`
- `06_Лаб4_команда/Киселев_API_ДТП/png/dynamic.png`
- `06_Лаб4_команда/Киселев_API_ДТП/png/landscape.png`
- `06_Лаб4_команда/Мехова_Backoffice/png/deployment.png`
- `06_Лаб4_команда/Мехова_Backoffice/png/dynamic.png`
- `06_Лаб4_команда/Мехова_Backoffice/png/landscape.png`
- `06_Лаб4_команда/Мехова_Backoffice/puml/common.inc`
- `06_Лаб4_команда/Мехова_Backoffice/puml/deployment.puml`
- `06_Лаб4_команда/Мехова_Backoffice/puml/dynamic.puml`
- `06_Лаб4_команда/Мехова_Backoffice/puml/landscape.puml`
- `06_Лаб4_команда/Романов_WebApp/png/deployment.png`
- `06_Лаб4_команда/Романов_WebApp/png/dynamic.png`
- `06_Лаб4_команда/Романов_WebApp/png/landscape.png`
- `06_Лаб4_команда/Романов_WebApp/puml/common.inc`
- `06_Лаб4_команда/Романов_WebApp/puml/deployment.puml`
- `06_Лаб4_команда/Романов_WebApp/puml/dynamic.puml`
- `06_Лаб4_команда/Романов_WebApp/puml/landscape.puml`
- `06_Лаб4_команда/Таган_тимлид/png/deployment_global.png`
- `06_Лаб4_команда/Таган_тимлид/png/dynamic_process.png`
- `06_Лаб4_команда/Таган_тимлид/png/landscape_global.png`
- `06_Лаб4_команда/Таган_тимлид/puml/common.inc`
- `06_Лаб4_команда/Таган_тимлид/puml/deployment_global.puml`
- `06_Лаб4_команда/Таган_тимлид/puml/dynamic_process.puml`
- `06_Лаб4_команда/Таган_тимлид/puml/landscape_global.puml`
- `06_Лаб4_команда/Усков_Worker_финансы/png/deployment.png`
- `06_Лаб4_команда/Усков_Worker_финансы/png/dynamic.png`
- `06_Лаб4_команда/Усков_Worker_финансы/png/landscape.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/png/er.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/png/kts_схема_КТС.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/png/seq_auth.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/png/seq_claim.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/png/seq_pay.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/png/ui1.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/png/ui2.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/png/ui3.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/png/ui4.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/png/ui5.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/png/ui6.png`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/puml/er.puml`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/puml/kts_схема_КТС.puml`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/puml/seq_auth.puml`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/puml/seq_claim.puml`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/puml/seq_pay.puml`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/puml/ui1.puml`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/puml/ui2.puml`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/puml/ui3.puml`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/puml/ui4.puml`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/puml/ui5.puml`
- `07_Курсовая_гл4_ER_последовательности_UI_КТС/puml/ui6.puml`
