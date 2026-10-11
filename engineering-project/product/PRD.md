# DepotFlow — Product Requirements Document v1.0

Платформа для сотрудников и корпоративных клиентов одного арендного оператора с несколькими складами. Мультиарендность — несколько независимых организаций оператора в одном SaaS, клиент принадлежит ровно одной организации. Проблема: обещанное наличие расходится с физическими активами, задержки оплаты и ремонта порождают ручные ошибки. Цель: непротиворечивый путь quote → reservation → authorization → handover → return → settlement с диагностируемыми отказами.

## Роли

| Роль | Разрешено | Запрещено |
|---|---|---|
| customer | поиск, свой checkout, свои bookings, отмена до выдачи, свои уведомления | чужие договоры, rates, capture/refund |
| operator | assets и выдача/возврат только назначенного depot | менять тарифы, роли, refund |
| finance | payment/ledger своей организации, refund с причиной | выдача или назначение роли |
| org_admin | membership, rates, audit своей организации | bypass state machine, ручное изменение ledger |
| service principal | только разрешённые internal endpoints/events | вход в UI и действия от имени customer без subject |

Одна активная роль membership; смена роли фиксируется с version. Admin также нуждается в operator membership для физической выдачи (смена роли); superuser обходы запрещены.

## Обязательный scope

F01–F20 — все обязательны. Приоритет P0: F01, F04–F12, F16–F18 (целостность и безопасность); P1: F02–F03, F13–F15, F19–F20 (полноценная эксплуатация). Priority означает порядок реализации, не право выкинуть функциональность. Полные stories в product/stories, machine registry requirements/functional.json.

Основные journeys: клиент находит модель и котировку, получает подтверждение либо понятную причину отказа; оператор видит складские jobs, выдаёт и принимает оборудование; finance разбирает неизвестный PSP результат и выполняет ограниченный refund; admin управляет тарифами, доступом и анализирует историю. Корректность — отсутствие двойного выделения, лишнего списания и межtenant утечек; success screen появляется лишь после authoritative business state.

## Правила продукта

EUR integer minor units; без налогов в core (цены учебные, не бухгалтерский расчёт). Целые qty 1..5; один model/depot/период на booking. Начало ≥ now+1h; duration 1h..30d; interval [start,end), UTC persistence, UI Europe/Tallinn explicit. Price snapshot на 15 min; hold на 10 min, не продлевается heartbeat. Booking сохраняет quote snapshot, Inventory выделяет конкретные assets. Рабочий день аренды — 24 h, округление вверх; DST не меняет длительность UTC. Sandbox authorization действительна 45d, максимум аренды30d. Partial pickup/return и перенос срока — advanced, не core. Все assets возвращаются одним актом.

Срок просрочки: ceil(max(0, return_at-end_at)/24h), grace15 min (если lateness ≤15 min, late_days0; иначе весь lateness округляется). late_charge=late_days*daily_minor*qty. Damage — целое 0..deposit_minor общей котировки, с заметкой; превышение или capture total > authorized -> manual_review. Capture только после return. Нереальные PSP/тарифы явно подписаны.

## Ограничения и допущения

Сервис Fulfillment фиксирует физический факт; потерянный ответ не отменяет состоявшуюся выдачу. При просроченном возврате asset становится unavailable; будущие committed bookings на этот asset получают reconciliation incident, оператор не выдаёт отсутствующий asset и организует ручное замещение/отмену с компенсацией. В core нет гарантии наличия при нарушении клиентом физического срока. Граница учебной и коммерческой инфраструктуры описана в operations/environments.md.

## Out of scope / Advanced

Маркетплейс, реальные карты, real invoices, налоговый движок, кредиты, оптимизация маршрутов, геолокация, multi-currency. Advanced: split return, partial capture, replacement saga, Kafka projection, multi-region. Эти расширения не заменяют обязательные failure scenarios.

## Success

Все F/N/A требования имеют evidence и независимый audit; нет автоматического обещания production-grade SLA. Система production-like: проектирует коммерческие проблемы и тренирует инженерный процесс в измеренной лаборатории.
