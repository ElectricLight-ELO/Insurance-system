 
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
 
title КОНТЕЙНЕРЫ: Система фиксации ДТП
 
' Настройка цветов для внешних систем (серый)
AddSystemTag("внешняя", $bgColor="#A9A9A9", $borderColor="#8A8A8A")
 
' Явно определяем тег для пунктирной линии
AddRelTag("пунктир", $lineStyle = DashedLine(), $lineColor = "#707070")
 
' === ВНЕШНИЕ УЧАСТНИКИ И СИСТЕМЫ ===
 
Person_Ext(expert, "Аварийный эксперт", "Сотрудник, выезжающий на место ДТП")
Person(client, "Клиент", "Участник ДТП")
 
System_Ext(ais_osago, "АИС ОСАГО", "Автоматизированная информационная система", $tags="внешняя")
System_Ext(email_sys, "E-mail система", "Внутренняя система обмена письмами", $tags="внешняя")
 
' === ГРАНИЦЫ СИСТЕМЫ ===
 
System_Boundary(fixation_system, "Web-сервис фиксации ДТП") {
 
    Container(terminal, "Служебный терминал", "Android", "Терминал подтверждения для фотографий на базе Android")
 
    Container(api, "API (FASTAPI)", "Python / FastAPI", "Обработка REST-запросов, актов фиксации ДТП")
 
    Container(worker, "Worker", "Python", "Асинхронная обработка задач, генератор PDF, скрипты")
    
    ContainerDb(object_storage, "Object Storage", "S3 / MinIO", "Хранение фотографий ДТП и подписей")
    
    ContainerDb(database, "Database", "PostgreSQL", "Хранение данных активных полисов и данных")
}
 
' === СВЯЗИ ===
 
' Внешние взаимодействия
Rel(expert, terminal, "Загрузка фотографий\nрезультатов осмотра и информации")
Rel(client, terminal, "Подпись")
Rel(client, api, "Электронный протокол осмотра", "PDF")
 
' Внутренние взаимодействия (внутри системы)
Rel(terminal, api, "Отправка результатов осмотра", "HTTPS, JSON")
Rel(api, object_storage, "Сохранение фото и подписей", "HTTPS, JSON")
Rel(api, worker, "Создание задач на обработку")
Rel(api, database, "Чтение и запись актов фиксации", "HTTPS, JSON")
Rel(api, ais_osago, "Проверка наличия ОСАГО", "HTTPS")
 
' Взаимодействия Worker
Rel(worker, database, "Забирает задачи в статусе new/pending sql")
Rel(worker, object_storage, "Чтение фото и подписей", "HTTPS")
Rel(worker, ais_osago, "Повторный запрос/регистрация при сбоях", "HTTPS, JSON")
Rel(worker, email_sys, "Запрос на отправку протокола", "HTTPS")
 
' ПУНКТИРНАЯ стрелка от E-mail системы к Клиенту
Rel(email_sys, client, "Отправка электронного протокола осмотра", $tags="пунктир")
 
@enduml