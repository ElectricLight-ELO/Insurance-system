@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
 
title КЛИЕНТ C4 CONTEXT
 
' Создаем тег "внешняя" для серых систем
AddSystemTag("внешняя", $bgColor="#A9A9A9", $borderColor="#8A8A8A")
 
' Явно определяем тег "пунктир" со стилем пунктирной линии
AddRelTag("пунктир", $lineStyle = DashedLine(), $lineColor = "#707070")
 
Person(client, "Клиент", "Пользователь, оформляющий полис")
System(payment_sys, "Платежная система", "Внешняя система проведения платежей", $tags="внешняя")
System(service, "Информационная система оформления ОСАГО (ИС ОСАГО)", "Cервис Осаго")
System(email_sys, "E-mail система", "Внутренняя система обмена письмами", $tags="внешняя")
System(ais_osago, "АИС ОСАГО", "Автоматизированная информационная система", $tags="внешняя")
 
Rel(client, service, "Вводит данные, выбирает опции,\nоплачивает и получает полис ОСАГО")
Rel(service, payment_sys, "Инициирует платеж,\nполучает статус оплаты")
Rel(service, email_sys, "Отправляет сведения на полис и чека")
Rel(service, ais_osago, "Передача КЗМ, регистрация полиса")
 
Rel(email_sys, client, "Доставка письма со ссылкой на полис и чеком", "email", $tags="пунктир")
 
@enduml