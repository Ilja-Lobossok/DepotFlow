"""Editable source of the assignment pack. Python 3.12+, standard library only."""
from pathlib import Path
import json, html, re, shutil
ROOT = Path(__file__).resolve().parents[1]
DOCS = {}
def write(path, text):
    p = ROOT / path; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip()+'\n', encoding='utf-8')
    if p.suffix == '.md': DOCS[path] = text.strip()
def dump(path, obj): write(path, json.dumps(obj, ensure_ascii=False, indent=2))

SOURCES = [
 ('R01','Wise Graduate Software Engineer','Tallinn; graduate','https://wise.jobs/job/graduate-software-engineer-in-tallinn-jid-2903','Expired explicitly; cohort September 2026','CS fundamentals, major programming language, review, communication. Language list is not a mandatory stack.'),
 ('R02','Wise API Experience Java','Europe; senior reference','https://jobs.smartrecruiters.com/Wise/744000063454628-senior-software-engineer-i-api-experience-java','Accessible posting; older indexed page, hiring status unconfirmed','Java/Spring Boot, public APIs, microservices, events, relational data, Kafka or similar. Senior expectations are a future depth reference.'),
 ('R03','Bolt Engineering careers','Tallinn; senior reference','https://bolt.eu/en/careers/teams/engineering/','Accessible employer careers page','Node.js/TypeScript, distributed systems and product algorithms; reinforces transferability, not a junior hiring guarantee.'),
 ('R04','Codeborne full-stack developer','Tallinn; mid-senior','https://codeborne.com/en/jobs/full-stack-developer-tallinn/','Accessible employer posting','Java/Kotlin or Svelte/Vue, TDD, pair work, client communication. React is not universal.'),
 ('R05','Tipico (Junior) Java Developer','Europe; junior','https://jobs.smartrecruiters.com/Tipico/744000136171599--junior-java-developer-m-f-x-?trid=7d1dcdfa-96a8-4e55-bb9c-0db211f5a9b3','Indexed employer posting; availability unconfirmed','Java backend, React frontend, first practical experience, review and end-to-end ownership.'),
 ('R06','Version 1 Junior Java Developer','UK; junior title, 2 years required','https://jobs.smartrecruiters.com/Version1/744000148946885-junior-java-developer','Accessible posting','Java APIs, Spring, Git, Maven, Jenkins, Azure desirable. Junior title does not mean zero experience.'),
 ('R07','LOGEX Junior Platform Engineer','Amsterdam; junior title, around 2 years','https://logex.recruitee.com/o/platform-engineer-1?lang=en','Accessible older indexed posting; availability unconfirmed','K8s/K3s, Linux, Terraform/Ansible, cloud. Platform work combines troubleshooting and delivery.'),
 ('R08','SEB Junior Software Platform Engineer','Solna; graduate/early career','https://jobs.eu.lever.co/seb/3ae41077-3709-4376-b54f-b47ab3af01b8','Accessible; deadline 2026-11-01 stated','CI/CD, testing, containers, IaC. Prior platform employment not required; listed tools are advantages, not all mandatory.'),
 ('R09','Capgemini Junior Cloud Engineer','Porto; junior title','https://careers.capgemini.com/job/Vila-Nova-de-Gaia-Junior-Platform-Engineer-%28Porto%29/1399964033/?feedId=388633&tcsource=apply','Indexed employer posting','Cloud, IaC, Linux, networking, containers and incident analysis; requirements include strong experience despite title.'),
 ('R10','Evolution React openings','Tallinn; mid-senior','https://careers.evolution.com/job/744000126042610/','Direct fetch 410 Gone; excluded from active evidence','Search snippet mentions React/TypeScript and delivery tooling; retained as a negative freshness check only.'),
 ('E01','Zalando: Simplicity by Distributing Complexity','Engineering; 2018-01-23','https://engineering.zalando.com/posts/2018/01/simplicity-by-distributing-complexity.html','Article read','Independent data ownership and derived views illustrate the costs of event driven data aggregation. Not a blueprint for this domain.'),
 ('D01','PostgreSQL range types','Official documentation','https://www.postgresql.org/docs/current/rangetypes.html','Read; page resolves to PostgreSQL 18','Range exclusion can prevent overlapping allocations; design exercise uses this invariant.'),
 ('D02','RabbitMQ confirms','Official documentation','https://www.rabbitmq.com/docs/confirms','Read','Publisher confirms and consumer acknowledgements are separate; they do not guarantee business exactly-once.'),
 ('D03','RabbitMQ reliability','Official documentation','https://www.rabbitmq.com/docs/reliability','Read','Connection loss may cause redelivery; consumers must tolerate duplicates.'),
 ('D04','Kubernetes probes','Official documentation','https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/','Read','Startup, readiness and liveness serve different purposes; do not restart the fleet for broker failure.'),
 ('D05','OpenTelemetry traces','Official documentation','https://opentelemetry.io/docs/concepts/signals/traces/','Read','Trace/span context connects causal work across services.'),
 ('D06','Spring Boot requirements','Official documentation','https://docs.spring.io/spring-boot/system-requirements.html','Read','Choose Java 21 and Boot 4.1 family, verify compatible libraries and pin exact patch at M01.'),
 ('D07','OpenAPI 3.1.1','Specification','https://spec.openapis.org/oas/v3.1.1.html','Read','Machine-readable HTTP contracts, JSON Schema data descriptions.'),
 ('D08','AsyncAPI 3.0','Specification','https://www.asyncapi.com/docs/reference/specification/v3.0.0','Read','Per-application send/receive contracts; channels do not by themselves define queue topology.'),
 ('D09','Keycloak OIDC','Official documentation','https://www.keycloak.org/securing-apps/oidc-layers','Read','OIDC provider separates authentication from application membership authorization.')
]
write('research/market-study.md', '''# Research & product selection — 11 October 2026

Дата проверки: 2026-10-11, Europe/Tallinn. Метод: целевая качественная выборка страниц работодателей и официальной документации. Это не перепись вакансий и не статистика долей рынка. Поиск смещён к Java, TypeScript и platform; результаты не доказывают превосходство языка или вероятность трудоустройства. География, разрешение на работу, язык и образование требуют отдельной проверки при реальном отклике.

## Наблюдения и выводы

R01 показывает ценность фундаментальных знаний и объяснения решений. R02–R06 дают основания тренировать JVM, SQL, API, review и frontend; senior-позиции используются только как ориентир роста. R07–R09 показывают отдельный путь platform: Linux, сети, IaC, контейнеры, инциденты. Название Junior иногда соседствует с требованием 2 лет, поэтому диплом проекта не равен опыту работы. R10 исключена как закрытая страница. Малое число локальных entry-level находок нельзя трактовать как отсутствие спроса.

Главный учебный результат: объяснимые транзакции, контракт API, диагностика сбоя и воспроизводимый deployment. Количество логотипов инструментов не является результатом. Java/Spring выбирается для core-domain; React/TypeScript — для UI; один TypeScript Notification сервис даёт межъязыковую контрактную практику. Kafka не добавляется в основную систему: RabbitMQ лучше соответствует командам и ограниченной нагрузке, Kafka изучается в сравнительной лаборатории.

## Сравнение предметных областей

Оценки 1–5 — авторское суждение, не измерения рынка. Критерии: коммерческий реализм (C), естественные границы (M), распределённость (D), бизнес-правила (B), четыре направления (E), соответствие задачам вакансий (J), выполнимость одному (S), защита (I). Вес каждого одинаковый; сумма не скрывает trade-offs.

| Вариант | C | M | D | B | E | J | S | I | Итог /40 | Ограничение |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| DepotFlow: B2B аренда оборудования |5|5|5|5|5|4|4|5|38|Временные интервалы и физический возврат усложняют тесты|
| ColdRoute: холодовая логистика |5|5|5|5|5|4|2|5|36|Телеметрия и маршрутизация быстро расширяют scope|
| PermitDesk: разрешения на строительство |5|3|3|5|4|4|4|4|32|Много workflow, меньше естественных конкурентных ресурсов|
| SeatWave: билеты на мероприятия |5|4|5|4|5|4|4|4|35|Хорошая конкуренция, но предметная область часто повторяет учебные проекты|

Выбран DepotFlow: ограниченные физические ресурсы, срок удержания, необратимая выдача и отдельно управляемые платежи дают разные причины распределённости. Это вымышленный продукт с реалистичными правилами, а не утверждение о внутренней архитектуре существующей компании. Для маленького коммерческого стартапа монолит мог бы стоить меньше; здесь микросервисы — явная цель capstone, а границы выбраны по ответственности, а не ради контейнеров.

Исключены: Match Me, marketplace между независимыми арендодателями, реальная обработка карт, налоги по странам, бухгалтерская сертификация, оптимизация маршрутов, IoT. Sandbox PSP и почтовый sink обязательны; настоящие деньги и персональные данные не нужны.

## Источники и состояние

''' + '\n\n'.join(f'### {sid} — {title}\n\n{scope}. {status}.\n\n{note}\n\nИсточник: [{title}]({url}). Проверено 2026-10-11.' for sid,title,scope,url,status,note in SOURCES))
dump('research/sources.json',[dict(id=i,title=t,scope=g,url=u,status=s,notes=n,checked='2026-10-11') for i,t,g,u,s,n in SOURCES])

SERVICES = [
 dict(id='tenancy',name='Tenancy',purpose='Организации, членство, роли и допуск к складам',boundary='Не хранит пароли; Keycloak аутентифицирует, Tenancy решает бизнес-доступ.',tables={'organizations':'id, name, status, version','memberships':'id, org_id, subject_id, role, depot_id?, status, version','audit_entries':'id, org_id, actor_id, action, target_id, occurred_at'},publishes=['membership.changed'],consumes=[],failure='Недоступность Tenancy блокирует новые бизнес-команды (503), чтения возможны с membership snapshot не старше 60 s.',scale='Stateless HTTP replicas; membership lookup indexes; no shared auth cache without bounded revocation.',metrics='authorization_denied_total; membership_check_seconds',tests='Два tenant, отозванная роль, чужой depot, audit without token data'),
 dict(id='catalog',name='Catalog',purpose='Модели оборудования, тарифы и неизменяемые котировки',boundary='Не утверждает наличие экземпляров и не владеет денежными проводками.',tables={'models':'id, org_id, name, category, active, version','rates':'id, org_id, model_id, daily_minor, deposit_minor, currency, valid_from, version','quotes':'id, org_id, model_id, depot_id, start_at, end_at, quantity, days, daily_minor, rental_minor, deposit_minor, currency, expires_at, rate_version'},publishes=['catalog.changed'],consumes=[],failure='При падении Catalog новый checkout не начинается; подтверждение уже сохранённой котировки не требует повторного расчёта.',scale='Cache-aside Redis for model lists only; immutable quotes stored in PostgreSQL.',metrics='quote_created_total; catalog_cache_hit_total; quote_calculation_seconds',tests='Изменение тарифа после quote, округление вверх, timezone, quantity limits'),
 dict(id='inventory',name='Inventory',purpose='Экземпляры, временные allocations, holds, ремонт и доступность',boundary='Единственный авторитет по пересечению интервалов; Availability UI — подсказка.',tables={'depots':'id, org_id, name, timezone','assets':'id, org_id, model_id, depot_id, serial, state, version','holds':'id, org_id, booking_id, expires_at, status, version','allocations':'id, org_id, asset_id, hold_id?, booking_id?, kind, period, active, version','maintenance_jobs':'id, org_id, asset_id, reason, status, version','release_tombstones':'id, org_id, booking_id, reason, created_at'},publishes=['hold.created','hold.rejected','hold.expired','allocation.committed','allocation.released','asset.unavailable'],consumes=['booking.reserve-requested','booking.commit-requested','booking.release-requested','fulfillment.returned','fulfillment.handed-over'],failure='Если Inventory недоступен, booking остаётся pending; никогда не предполагает успешный резерв по timeout.',scale='Выбор экземпляров в стабильном порядке; locks и exclusion invariant; replicas не обходят БД.',metrics='allocation_conflict_total; hold_expired_total; allocation_transaction_seconds',tests='100 checkout на один asset; hold expiration/commit race; ремонт против резерва'),
 dict(id='booking',name='Booking',purpose='Договор аренды, saga подтверждения и отмены, проекция истории',boundary='Оркестратор процесса; не меняет чужие таблицы и не решает наличие сам.',tables={'bookings':'id, org_id, customer_id, quote_id, quote_snapshot, status, version, created_at','sagas':'id, org_id, booking_id, phase, deadline_at, cancel_requested, version','timeline_entries':'id, org_id, booking_id, source_event_id, type, at'},publishes=['booking.reserve-requested','booking.commit-requested','booking.release-requested','booking.confirmed','booking.cancelled','billing.authorize-requested','billing.void-requested','billing.settle-requested'],consumes=['hold.created','hold.rejected','hold.expired','allocation.committed','allocation.released','payment.authorized','payment.failed','payment.voided','payment.captured','payment.refunded','fulfillment.handed-over','fulfillment.returned'],failure='Saga state persists before publishing; restart resumes. Unknown payment state leads to reconciliation, not a second charge.',scale='Scheduler row leases; optimistic version; event handlers per booking serialized at DB.',metrics='saga_pending_seconds; saga_reconciliation_total; bookings_confirmed_total',tests='Поздняя авторизация, cancel vs commit, crash after write, event reordering'),
 dict(id='billing',name='Billing',purpose='Sandbox payment intent, authorization, capture, refund и ledger',boundary='Только симулированный PSP; никакие PAN/CVV, реальные платежи или обещания юридической корректности.',tables={'payment_intents':'id, org_id, booking_id, customer_id, authorized_minor, captured_minor, refunded_minor, pending_refund_minor, status, provider_key, version','payment_operations':'id, org_id, intent_id, kind, amount_minor, provider_key, status, attempt, version','provider_events':'id, provider_event_id, intent_id, signature_valid, received_at','ledger_entries':'id, org_id, intent_id, operation_id, kind, amount_minor, created_at'},publishes=['payment.authorized','payment.failed','payment.voided','payment.captured','payment.refunded'],consumes=['billing.authorize-requested','billing.void-requested','billing.settle-requested'],failure='Timeout PSP означает UNKNOWN. Запрос по provider_key и reconcile; не трактовать как decline.',scale='Intent lock + unique operation; webhook rate limit; PSP call outside long DB lock.',metrics='psp_request_seconds; payment_unknown_total; reconciliation_age_seconds',tests='Duplicate webhook, invalid signature, capture+refund bounds, provider processed but response lost'),
 dict(id='fulfillment',name='Fulfillment',purpose='Складская выдача, inspection возврата и акт состояния',boundary='Подтверждает физическое действие; не запускает новую аренду и не переписывает hold.',tables={'jobs':'id, org_id, booking_id, customer_id, depot_id, asset_ids, start_at, end_at, status, version','handover_records':'id, org_id, job_id, asset_ids, actor_id, occurred_at','return_reports':'id, org_id, job_id, condition, late_days, damage_minor, notes, version','booking_projection':'booking_id, org_id, status, last_version, updated_at'},publishes=['fulfillment.handed-over','fulfillment.returned'],consumes=['booking.confirmed','booking.cancelled'],failure='При stale projection перед выдачей проверить Booking синхронно; при его недоступности выдачу блокировать. Возврат уже выданного job записывается локально.',scale='Optimistic job version; one handover per job; warehouse-specific replicas unnecessary initially.',metrics='handover_conflict_total; fulfillment_projection_lag_seconds; return_processing_seconds',tests='Cancel vs handover fence; wrong depot operator; double return; damage escalation'),
 dict(id='notification',name='Notification',purpose='Внутренние уведомления, доставка email и предпочтения',boundary='Отказ уведомления не откатывает аренду; история аренды остаётся в Booking.',tables={'preferences':'id, org_id, subject_id, email_enabled, version','notifications':'id, org_id, subject_id, source_event_id, title, read_at','deliveries':'id, org_id, notification_id, channel, status, attempt, next_attempt_at'},publishes=[],consumes=['booking.confirmed','booking.cancelled','fulfillment.returned','payment.refunded'],failure='Почта недоступна: retries, DLQ, UI notification сохранён. Email exactly-once не обещается.',scale='TypeScript Node.js workers; bounded concurrency, own Postgres and inbox.',metrics='delivery_failed_total; notification_queue_age_seconds',tests='Duplicate event creates one notification; sink timeout; tenant isolation of SSE')
]
dump('architecture/services.json', SERVICES)

# User stories are the canonical functional requirement registry.
# title, role, intent, prerequisites, main, alternative, errors, acceptance, milestone, screens
STORIES = [
 ('F01','Доступ организации','org_admin','Разделить данные компаний','OIDC session; active organization','Пригласить участника; назначить одну роль и при необходимости depot','Отозвать membership; следующий command запрещён','Чужой org или depot -> 404/403','Given A/B; When member A GET booking B; Then 404 и тело без PII. Revocation запрещает команды сразу после authoritative check, чтения ≤60 s.','M02','login,team'),
 ('F02','Каталог и тариф','org_admin','Управлять арендным предложением','F01; модель принадлежит tenant','Создать model и rate в EUR minor units; заменить rate новым version','Deactivate model скрывает новые quotes, не ломает существующие','Нулевая/отрицательная стоимость или inactive model -> 422','Given rate 2500; When rate changes to 3000 after quote; Then existing quote uses 2500 until expiry.','M03','catalog,rate'),
 ('F03','Поиск доступности','customer','Найти модель на срок','F02; depot active','Выбрать depot, start/end, quantity; фильтр категории, cursor pagination','Нет единиц -> empty state; Redis down -> SQL','start>=end, quantity вне 1..5 ->422','When 26 models with page limit 25; Then second cursor returns last item without duplicate. Availability never guarantees allocation.','M04','catalog,availability'),
 ('F04','Котировка','customer','Получить неизменяемую цену','F03; период 1h..30d, начало ≥ now+1h','Quote expires after 15 min; days=ceil(duration/24h); quantity multiplied','Quote expired -> refresh with explicit consent if amount changes','Вход содержит decimal money or negative duration ->422','Given 25 h, qty2, rate2500, deposit10000 per unit; Then days2, rental10000, deposit20000, total authorization30000.','M03','quote,checkout'),
 ('F05','Временный резерв','customer','Не продать один asset дважды','F04; valid quote','Booking pending -> reserve command; Inventory holds exact assets 10 min','Недостаточно units -> rejected; no partial holds','100 concurrent commands contend -> one wins for qty1/one asset','Given one asset; When 100 unique bookings overlap; Then exactly 1 hold, 99 rejections, zero overlapping active allocations.','M05','checkout,pending'),
 ('F06','Подтверждение аренды','customer','Получить договор после авторизации','F05; PSP sandbox','HoldCreated -> authorize; Authorized -> commit; Committed -> confirmed','Transient faults leave pending/reconciling; customer sees status','Expiry before commit -> release and void; never confirm expired hold','Given authorization succeeds and allocation commits; Then one confirmed booking, one active allocation, one authorization; 10 duplicate events change none of these counts.','M07','pending,booking'),
 ('F07','Идемпотентность команд','customer','Безопасно повторить потерянный ответ','F01; Idempotency-Key','Store request hash and durable response per org+subject+route+key 24h','Same hash returns same resource/status; processing ->202','Same key different body ->409 idempotency_mismatch','When retry 20 times after response loss; Then one booking and one operation; tenant B may reuse same key independently.','M05','checkout'),
 ('F08','Отмена до выдачи','customer','Освободить резерв и деньги','F06; pending or confirmed, not handed over','Record cancellation intent under booking lock; saga releases allocation and voids authorization','Late authorized event triggers void even after cancellation','Handover claimed or handed_over ->409 cannot_cancel','When cancel races allocation commit; Then terminal cancelled eventually has no active allocation and net captured0; timeout alone is not cancelled completion.','M08','cancel,booking'),
 ('F09','Складская выдача','operator','Передать конкретные assets клиенту','F06; same depot; now in pickup window start-1h..end','Claim handover atomically in Booking then Fulfillment records act','Lost response: query claim, resume same job, never release automatically','Missing allocation, revoked operator, cancellation won ->409/403','When cancel and handover claim race; Then exactly one wins. Double handover returns original act; different payload ->409.','M09','warehouse,handover'),
 ('F10','Возврат и inspection','operator','Сохранить состояние оборудования','F09; active job','Record return once; condition good/damaged; Inventory releases or quarantines; Booking starts settlement','Offline dependencies -> queued event; partial returns excluded core','Damage above deposit -> manual_review, no automatic extra debit','When return event delivered 10 times; Then one report, one release, one settlement; damaged asset not bookable until repair.','M09','return,booking'),
 ('F11','Завершение оплаты','customer','Списать аренду и вернуть остаток','F10; valid authorization','Capture rental+late+damage within authorized bound; remainder void; ledger persists','Provider unknown -> reconciling and operator alert','Overdeposit total -> manual_review; never overcapture','Given authorized15000, rental5000, late2500, damage1000; Then capture8500 and void remaining6500, captured-refunded=8500.','M10','billing,booking'),
 ('F12','Возврат списанных средств','finance','Исправить ошибочное списание','F11; finance role; captured>refunded','Reason mandatory; idempotent refund ≤ remaining captured; webhook verifies result','Timeout queries PSP before retry','Customer role ->403; refund over remainder ->422','When two concurrent full refunds; Then total refunded ≤ captured and one succeeds; second conflicts.','M10','billing,refund'),
 ('F13','Ремонт','operator','Блокировать неисправный экземпляр','F01; assigned depot','Create maintenance allocation for non-rented asset; complete repair explicitly','Future reservations conflict -> reject and show affected booking IDs for dispatcher','Already handed_over ->409; cannot delete existing bookings','When maintenance period overlaps a committed booking; Then409 and no maintenance insert; after successful repair new hold is permitted.','M04','fleet,maintenance'),
 ('F14','Уведомления и realtime','customer','Увидеть изменения без повторного checkout','F06; Notification running','Durable notification, SSE with cursor, email sink retry','SSE disconnected -> reconnect then HTTP snapshot; email fail does not fail booking','Cross-tenant SSE cursor ->404; unknown cursor -> fresh snapshot','Given confirmed event duplicated; Then one UI notification; SSE reconnect recovers latest state; email failure leaves confirmed.','M11','notifications,booking'),
 ('F15','История и audit','org_admin','Объяснить изменения процесса','F01; commands/events exist','Timeline with source event and correlation; auth decisions audit separately','Read projection lag displayed with updated_at','Secrets, tokens, full email never written to telemetry','When investigate failed booking; Then actor, before/after state, correlation and saga phase are recoverable; timeline rows unique by source event.','M12','booking,audit'),
 ('F16','Обновление конкурирующих форм','operator','Не потерять изменения коллеги','F13; resource version','If-Match version on modifications; 412 with refetch action','User reloads and explicitly repeats action','Missing If-Match ->428; stale ->412','When two forms edit same asset at v3; Then first creates v4, second412 and cannot overwrite.','M04','fleet,maintenance'),
 ('F17','Контракты и эволюция','engineer','Поставлять сервисы независимо','M06; v1 consumers','Add optional field; provider and old consumer contract suite run','Breaking meaning -> v2 route/event, overlap deployments','Required field removal or enum narrowing -> CI failure','Given old consumer fixture; When optional field added; Then both deserialize; breaking fixture rejected before release.','M13','contracts'),
 ('F18','Восстановление после сбоя','operator','Довести зависшие операции до результата','M08; broker and PSP faults injectable','Inspect saga and inbox/outbox; controlled DLQ replay retains event ID','Poison payload quarantined with original metadata','Blindly mark success or new charge -> forbidden','Given crash after DB commit before ACK; When restarted and replayed; Then one business effect and no lost transition.','M14','operations'),
 ('F19','Независимая поставка','engineer','Менять сервис без полного релиза','M13; images pinned','Pipeline builds changed service + reverse contract dependents; deploy digest, smoke, rollback','Failed readiness -> old deployment remains','Migration destructive in same release -> blocked','When deploy Notification only; Then six core service digests stay unchanged; rollback restores prior image without DB loss.','M16','operations'),
 ('F20','Резервное копирование','engineer','Восстановить данные с измеренным ущербом','M15; synthetic workload','Backup all owned stores and record cutover times; restore to isolated namespace; reconcile saga/provider','Unequal backup timestamps -> report and recovery queue','Restore into active prod namespace -> forbidden','When restore controlled checkpoint; Then known booking counts, ledger balance and allocation invariants match checkpoint; measured RTO≤30min and snapshot RPO≤24h.','M17','operations')
]
stories=[]
for sid,title,role,intent,pre,main,alt,err,ac,m,screens in STORIES:
    deps = re.findall(r'F\d{2}|M\d{2}',pre)
    stories.append(dict(id=sid,title=title,role=role,goal=intent,prerequisites=pre,main=main,alternative=alt,errors=err,acceptance=ac,milestone=m,screens=screens.split(','),depends=deps))
    write(f'product/stories/{sid}.md',f'''# {sid} — {title}

## Context & business goal
Как {role}, хочу: {intent}.

## Preconditions
{pre}. Выполнить проверку auth/session/tenant до доступа к данным. Пользовательские команды идут через gateway, service credentials не заменяют customer identity.

## Expected behavior / Main scenario
{main}.

## Alternative scenarios
{alt}.

## Error scenarios
{err}. UI показывает стабильный problem code, correlation ID и разрешённое действие. Не раскрывает чужие идентификаторы или stack trace.

## Acceptance criteria
{ac}

Записать автоматизированный тест с ID {sid}, fixture version и фактическим результатом. Снимок UI — дополнение к проверке состояния, а не доказательство транзакции.

## Dependencies and implementation task
{', '.join(deps) or 'M01'}; этап {m}; экраны: {screens}. Отдельный PR с review контракта и failure evidence. Для повторных команд и событий действуют общие правила contracts/README.md.
''')
dump('requirements/functional.json', stories)
write('product/PRD.md', '''# DepotFlow — Product Requirements Document v1.0

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
''')

NFR = [
 ('N01','Latency','На lab-standard: 20 virtual users, 10 min after 2min warmup; read p95≤300ms, command acceptance p95≤500ms; saga completion p95≤5s при здоровом PSP; error<1% excluding expected409/422.','M14'),
 ('N02','Integrity','100 concurrent overlapping bookings on one asset produce exactly one committed allocation. Zero overlap, overcapture and duplicate refund across 10k duplicate/reordered deliveries.','M08'),
 ('N03','Tenant isolation','Two organizations × all role/endpoint pairs; no foreign records, events, SSE or cache entries; 401/403/404 verified before access.','M02'),
 ('N04','Recovery','Broker outage120s, consumer killed after DB commit beforeACK; pending saga reconciles ≤120s after recovery for 100 bookings; DLQ poison remains quarantined.','M14'),
 ('N05','Observability','100% synthetic test traces sampled; booking→outbox→consumer→PSP causality queryable; logs correlate; metrics have no booking/customer label.','M12'),
 ('N06','Availability target','Lab SLO 99% successful eligible commands over 1h controlled run (denominator excludes auth/validation/conflict; includes dependency5xx). No claim about monthly production availability.','M14'),
 ('N07','Security','TLS on ingress and internal production-like traffic, JWT issuer/audience/expiry checked, secrets absent repository/logs, least-privilege DB/broker roles; security scenario suite passes.','M15'),
 ('N08','Delivery independence','Seven service images and DB migration streams; notification-only release changes no other digest; each service tests/builds/deploys without importing other business implementation.','M16'),
 ('N09','Accessibility','Keyboard complete customer checkout and operator return; visible focus; labels/errors; no color-only state; contrast normal text≥4.5:1; 360px without horizontal page scroll.','M11'),
 ('N10','Backup','Snapshot RPO target≤24h; measured isolated restore RTO≤30min for fixture dataset; reconnect mismatched service snapshots through reconcile, report unrecoverable delta.','M17'),
 ('N11','Data lifecycle','Synthetic users only; auth logs7d, telemetry7d, notifications30d, inbox/idempotency24h minimum with replay rules; booking/ledger retained for lab history; scrub demo emails on exports.','M15'),
 ('N12','Reproducibility','Clean lab host builds pinned images/contracts; bootstrap docs checked by reviewer; no mandatory external cloud, CDN or paid integration.','M18')
]
dump('requirements/nonfunctional.json',[dict(id=i,title=t,acceptance=a,milestone=m) for i,t,a,m in NFR])
write('requirements/nonfunctional.md','# Nonfunctional requirements\n\nПороги — учебные design targets, не измеренные показатели готового приложения.\n\n'+ '\n\n'.join(f'## {i}: {t}\n\n{a}\n\nЭтап: {m}. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.' for i,t,a,m in NFR))

PROCESS = [
 ('P01','Quote','customer; Catalog', 'active model/rate; trusted org membership', 'Validate UTC interval, qty; read rate in one transaction, snapshot price and expires_at. Return201 quote ID.', 'ACTIVE→EXPIRED by time; immutable body. Expired reuse422. Concurrent rate update cannot mix deposit/rental versions.', 'Retry create same key returns same quote. Cancel has no side effect; no money reserved. Catalog/DB fail503; UI re-quotes only after user consent.'),
 ('P02','Reserve','Booking → Inventory','persisted pending booking; valid quote snapshot', 'Publish reserve-requested via outbox; Inventory selects qty assets in ID order, locks asset rows, checks maintenance and allocation overlap, commits all-or-nothing hold+allocation+outbox.', 'REQUESTED→HELD or REJECTED; HELD→COMMITTED/EXPIRED/RELEASED. Tenant+asset+overlap exclusion, maintenance same allocation table. Failure to acquire any unit rolls back all.', 'Command identity booking_id. Multiple identical commands return same outcome event with stable ID/outbox identity; different parameters409. Expire sweep locks hold, sets allocation inactive; time guard on commit wins over delayed sweep.'),
 ('P03','Authorize & commit','Booking → Billing → Inventory','Held; no cancel requested; deadline=min(holdExpiry, sagaDeadline)', 'Billing authorizes rental+deposit using provider_key=booking+authorize:v1. Save authorized result/outbox. Booking publishes commit; Inventory under hold lock checks DB time<expires_at and alloc active; emits committed.', 'Booking PENDING→CONFIRMED only after allocation.committed AND authorized intent correlation. Expiry or rejection→COMPENSATING→CANCELLED/FAILED after release+void evidence.', 'PSP call may succeed while response lost: UNKNOWN, reconcile query by key; never generate new provider key. Late authorized after compensation -> void. Late committed while cancel intent -> release. Terminal state suppresses stale forward transitions.'),
 ('P04','Cancel','customer; Booking saga','own booking pending/confirmed; no handover claim', 'Atomic booking lock records cancel_requested and version; emit release+void commands if corresponding steps exist. Confirm completion only with observed allocation released and intent voided/no intent.', 'PENDING/CONFIRMED→CANCELLING→CANCELLED; concurrent handover claim→409. No cancellation after irreversible handover.', 'Repeated same cancellation returns same intent. Partial dependency failure leaves CANCELLING and reconciliation age visible; deadline does not imply compensation success. Cancel-before-hold sets tombstone to reject later hold/commit.'),
 ('P05','Handover fence','operator; Fulfillment + Booking','same depot, confirmed, active allocation, within pickup window', 'Fulfillment calls Booking claim with job_id and expected version. Booking atomic CONFIRMED→HANDOVER_CLAIMED; cancel now forbidden. Fulfillment persists physical act and event; Booking becomes IN_USE after event.', 'CONFIRMED→HANDOVER_CLAIMED→IN_USE. Claim idempotent per job; another job409. Claim without completed act after timeout→MANUAL_REVIEW, no automatic release.', 'Before physical transfer verify exact serial IDs locally against immutable confirmed allocation snapshot. Lost claim response re-query; never hand over on timeout. Operator must explicitly resolve claim incident; no TTL unlock of possible physical transfer.'),
 ('P06','Return & quarantine','operator; Fulfillment → Inventory','handover act present; same depot; all assets', 'One transaction return report+jobReturned+outbox. Inventory marks original allocation inactive, good asset READY, damaged asset QUARANTINED with maintenance block. Emits allocation.released.', 'Job IN_USE→RETURNED; Booking IN_USE→SETTLING. Asset READY→RENTED→READY/QUARANTINED. Out-of-order return before handed-over event requires entity lookup/parking.', 'Unique report per job; duplicate same command same report, different body409. If future allocation overlaps new quarantine, do not erase it: mark asset unavailable, incident and notify Booking to stop handover. Settlement blocked until release acknowledged.'),
 ('P07','Settle','Booking → Billing','return report and allocation release; authorized intent', 'Calculate immutable settlement from quote and return. Capture cost≤authorized; void unused authorization. Persist operation IDs/ledger; reconcile unknown PSP separately.', 'AUTHORIZED→CAPTURE_PENDING→CAPTURED or UNKNOWN; excess→MANUAL_REVIEW. Booking SETTLING→COMPLETED only after captured + remainder void or full void for zero cost.', 'Duplicate settlement operation returns prior amount; changed amount409. Capture+void must reconcile independently. Failure does not reallocate returned equipment. Customer sees settlement pending; no phantom complete.'),
 ('P08','Refund','finance; Billing','captured remainder>0; reason and If-Match', 'Lock intent, reserve refundable amount for pending operation, persist request; invoke PSP stable key outside lock; finalize ledger from response/webhook.', 'CAPTURED→REFUND_PENDING→PARTIALLY_REFUNDED/REFUNDED; UNKNOWN waits reconciliation. captured-refunded-pending_refunds≥0 invariant.', 'Concurrent full refunds cannot each reserve same remainder. Cancel refund before provider call optional; after call do not assume cancellation. Duplicate signed webhook unique provider_event_id; conflicting payload quarantined.'),
 ('P09','Repair','operator; Inventory','asset not rented; no conflicting committed interval','Under asset lock create maintenance allocation, asset QUARANTINED; repair records reason and completed inspection; deactivate maintenance block and mark READY.', 'READY→QUARANTINED→READY; cannot jump RENTED→READY without return. Future reservation conflicts return409 with dispatcher action.', 'Concurrent maintenance/hold share asset lock and exclusion invariant. Retry same key same maintenance job; changed reason conflicts. Operator access depot-scoped.'),
 ('P10','Notification','Notification','recognized event; valid tenant and subject','Inbox dedupe + notification + delivery plan atomic; sender retries mail sink with stable Message-ID; UI SSE sends IDs and cursor.', 'delivery PENDING→SENT or RETRY→DLQ; read_at independent. Projection versions only advance.', 'Duplicates do not produce duplicate UI rows, but external email can duplicate after ambiguous delivery. Retry 5 attempts; inbox replay policy required when retention reached. Disconnect uses HTTP snapshot, no correctness dependency on SSE.')
]
write('product/business-processes.md', '''# Business logic — authoritative process specification

Все часы сохраняются в UTC; deadline проверяет время БД, не браузера. IDs UUID; внешние ссылки принадлежат org. Чтение чужого объекта даёт404; запрещённая операция над своим —403. Проверка membership Tenancy синхронная на каждой изменяющей business command; кеш чтений≤60s. State transition и outbox пишутся одной транзакцией владельца. Inbox уникален (consumer,event_id); ack только после commit. Ниже правила обязательны совместно, не альтернативные варианты.

''' + '\n\n'.join(f'## {i} — {title}\n\n**Actors / authorization:** {actor}.\n\n**Initial conditions:** {pre}.\n\n**Actions / validation:** {act}\n\n**States / concurrency / forbidden transitions:** {state}\n\n**Retries / cancellation / partial failure / expected outcome:** {fail}' for i,title,actor,pre,act,state,fail in PROCESS) + '''

## Booking state machine

PENDING → CONFIRMED | COMPENSATING | CANCELLING; CONFIRMED → HANDOVER_CLAIMED | CANCELLING; HANDOVER_CLAIMED → IN_USE | MANUAL_REVIEW; IN_USE → SETTLING; SETTLING → COMPLETED | MANUAL_REVIEW; CANCELLING/COMPENSATING → CANCELLED/FAILED only after compensation evidence. FAILED/CANCELLED/COMPLETED terminal for forward business changes; late events can still cause compensating commands and audit rows. Refund never changes COMPLETED booking back to SETTLING. Manual review resolutions require reason, role and bounded state transition; no arbitrary status field setter API.

## Event ordering rule

Events carry producer aggregate_version and event_id; facts may arrive late. Consumers dedupe by ID and check event-specific prerequisites. Full snapshot projections ignore lower version; business facts are not discarded solely for low version (a late authorization still needs void). Gap -> park event with reason and perform authoritative GET; retry then DLQ if schema invalid. Commands have command_id plus expected correlation, idempotent by business operation; cancellation tombstone prevents resurrection. No total order across services.

## Physical overrun

Rental interval conflict guarantees promises based on scheduled return, not physically timely return. Sweep after end+15min for IN_USE assets marks unavailable and emits asset.unavailable; future job handover must reject absent asset. Inventory raises incident listing affected bookings. Dispatcher may cancel before claim or perform advanced replacement saga. Do not automatically refund/replace a physical asset silently. Test overrun against future committed allocation explicitly.
''')

write('architecture/system-design.md', '''# System design

Семь бизнес-сервисов: Tenancy, Catalog, Inventory, Booking, Billing, Fulfillment, Notification. PostgreSQL **database per service**, separate roles; один физический instance допустим только dev. Keycloak, gateway, Redis, RabbitMQ, observability — инфраструктура и не считаются бизнес-сервисами. Нет joins, SQL доступов или shared ORM entities между владельцами. Monorepo хранит контракты, но каждый service имеет own build/image/migration/release; общая библиотека допустима для logging/auth plumbing, не domain types.

## Sync / Async

Sync: OIDC discovery/JWKS; Tenancy membership checks; Catalog quote; Inventory availability; Booking handover claim; Billing GET reconciliation; пользовательские queries. Async: reserve/authorize/commit/release/void/settle commands и domain facts. RabbitMQ topic exchange depotflow.events + depotflow.commands; один durable queue per consumer, own DLQ; commands адресуются единственному владельцу, events fan-out. Booking — durable orchestrator saga, нет распределённой транзакции.

Outbox DB poller publishes persistent messages with mandatory routing + publisher confirm; mark published only after confirm; unroutable goes operator alert and stays pending. Crash between confirm and mark creates duplicate — ожидаемо. Inbox/business update/outbox commit атомарны; ack после commit. Доставка at-least-once, business effect effectively once under operation invariants; внешняя почта exactly-once не обещается. Local one-node broker не HA, three-node quorum lab даёт majority replication, не multi-region гарантию.

## Deadline and compensation

Reserve hold10min, quote15min. Saga begins only on valid quote; deadline=hold expiration after HoldCreated, initial request deadline30s to get hold; missing response triggers owner status query by booking_id. Authorize timeout5s; UNKNOWN reconciliation up to hold deadline then cancellation intent; late auth always void. Commit after expiration rejects even if sweeper lagged. Release command creates tombstone even before original reserve; a delayed reserve cannot resurrect booking. Saga scheduler leases rows and resumes after crash; terminal compensation checked from owner APIs, never inferred from timeout.

## Latency budget

External command acceptance ≤500ms target: membership150ms, local DB200ms, gateway overhead50ms, budget reserve100ms. Sync overall deadline2s, connect250ms, request1s for reads; handover claim1s. Max1 retry only for idempotent GET if remaining deadline; writes only stable operation key and owner lookup. PSP call timeout5s, open breaker after5 transport failures in30s, open30s, one half-open probe. Breaker is Billing adapter only: prevents exhausting worker slots, does not make UNKNOWN decline. Async transient retries 1/2/4/8/16s + full jitter[0,base], 5 attempts then DLQ; operator replay original event ID. Backlog oldest age alerts60s; flow control prefetch20, worker concurrency8 first measured then tuned.

## Storage / projections

Inventory authoritative concurrency; Booking owns status, Fulfillment physical act, Billing ledger. Read projections explicitly eventual; UI shows updated_at and pending, retry status via GET. Redis only Catalog model-list cache and gateway rate limiter, never allocation correctness. Cache keys include org+filter+cursor+rateVersion; TTL60s, invalidation on catalog.changed; quote calculates from DB, no stale pricing. Redis failure -> bounded SQL read, rate limit local emergency low cap with metric; never fail open on authorization.

## Scalability and evolution

Start with HTTP/REST (OpenAPI) and AMQP (AsyncAPI). No gRPC in core: no measured throughput justification and second transport hurts solo debugging. Comparative lab defines protobuf availability query, measures payload/latency and explains why it may remain out of core. Seven Java/Node services fit a lab with constrained memory profiles; do not claim autoscaling from replicas alone. Inventory can partition contention by depot; global date queries need index/query plans before sharding. Keep architecture same while implementing services sequentially.

## Source diagrams

architecture/diagrams/*.json are editable layout + semantic edges; *.svg are rendered standalone, captions specify design targets, not live deployments. Separate ER per owner and component/sequence/failure variants. diagrams/index.json maps sources to SVG and document.
''')

COMMON = '''
## Configuration / identity
Env names: SERVICE_PORT, DB_URL, DB_USER, DB_PASSWORD_FILE, AMQP_URL, OIDC_ISSUER, OIDC_AUDIENCE, OTEL_EXPORTER_OTLP_ENDPOINT, LOG_LEVEL. Private credentials via mounted secret, no committed .env with secrets. Validate required config at startup; store exact versions/digests in implementation lock file at M01. HTTP resource server JWT issuer/audience/expiry; internal credentials scoped per caller; tenant/subject contextual authorization survives gateway. Membership authoritative check on business writes. Broker ACL read/write only named queues/exchanges.

## Errors / health / deployment
RFC-style problem response: type, title, status, code, correlationId, violations (safe paths only); stable codes in contracts. 401 invalid auth;403 forbidden own resource;404 missing/foreign;409 business conflict;412 stale version;422 semantic validation;428 missing precondition;429 throttled;503 unavailable dependency. Liveness checks process only; startup validates migrations/config; readiness DB reachable, essential HTTP workers ready; broker outage marks async degradation and metrics, does not restart all services. Non-root container, readonly root filesystem, writable temp only, graceful drain30s; separate migration job; requests/limits measured in M15. Own image deployable without rebuilding peers.

## Private persistence / messaging
Each owner additionally has outbox(event_id UNIQUE, aggregate_id, payload, status, created_at), inbox(consumer,event_id UNIQUE, received_at), idempotency(org,subject,route,key UNIQUE, request_hash, response, expires_at). A service without outbound messages need not create outbox. Producer aggregate_version monotonic per aggregate; command_id stable across redelivery; consumer dedupe persists with business changes. No foreign-service DB permissions. Foreign IDs are opaque and validated via contract, no cross-DB FK.

## Test suite
Unit: pure transition rules, validation and money boundaries. Integration: PostgreSQL real transactions and migrations via Testcontainers; RabbitMQ ack/confirm tests where used. Contract: generated schema fixtures and provider/consumer compatibility. E2E: only exposed APIs and owned-state diagnostic reports, never foreign DB writes. Include tenant isolation, dependency timeout, duplicate and restart tests. Expose metrics without customer/booking high-cardinality labels; JSON logs with trace_id and correlation_id but no JWT or PII. See reviews/test-strategy.md.
'''
for s in SERVICES:
    tables='\n'.join('|'+t+'|'+cols+'|' for t,cols in s['tables'].items())
    write(f"architecture/services/{s['id']}.md",f'''# {s['name']} — service passport

## Responsibility / boundary
{s['purpose']}. {s['boundary']}

## Stack
{'Node.js current supported LTS at M01, TypeScript strict, Fastify, pg, amqplib' if s['id']=='notification' else 'Java21, Spring Boot4.1 family, Maven wrapper, Spring Security, JDBC explicit transactions, Flyway; pin patch and image digests at M01'}.
JDBC selected over automatic ORM cascades for visible locking and aggregate transitions; ORM alternative allowed after ADR preserving SQL invariants.

## Data ownership / schema
Database: {s['id']}_db. Role: {s['id']}_app. No credentials for other owners.

| Table | Logical columns |
|---|---|
{tables}

Logical model, types/indexes/constraints in data/models/{s['id']}.md and ER source. Migration implementation remains student work.

## HTTP contract
[OpenAPI](../../contracts/openapi/{s['id']}.json); public and internal operations clearly tagged. The API is a design specification, not a running server.

## Events / dependencies
Publishes: {', '.join(s['publishes']) or 'none'}. Consumes: {', '.join(s['consumes']) or 'none'}.
[Per-service AsyncAPI](../../contracts/asyncapi/{s['id']}.json). Dependencies follow named commands/GETs; all services depend on Tenancy for mutation authorization, Keycloak JWKS, own DB and telemetry. Catalog/Notification use Redis/SSE as specified; Billing alone calls PSP; Fulfillment claims Booking; Booking fetches immutable Catalog quote snapshot and owner recovery status.

## Failure behavior
{s['failure']}

## Metrics and scaling
{s['metrics']}. {s['scale']}

## Service-specific checks
{s['tests']}.
{COMMON}
''')

MODEL_EXTRA = {
 'tenancy':'UNIQUE(org_id,subject_id); membership role CHECK listed role; depot nullable except operator. Index active memberships by(org,subject), audit(org,occurred_at). Tenancy does not FK to Inventory depot; validate authoritative depot GET on assignment.',
 'catalog':'Rates immutable; INDEX(org_id,model_id,valid_from DESC). Quote stores all money amounts as BIGINT≥0, currency CHECK EUR, timestamps TIMESTAMPTZ, days INTEGER≥1. Quote retains rate_version; model delete forbidden once quoted, soft deactivate.',
 'inventory':'allocations.period TSTZRANGE [), bounded, nonempty; CHECK start<end. EXCLUDE GiST(org_id WITH =,asset_id WITH =,period WITH &&) WHERE(active); btree_gist extension prerequisite. All reserve/maintenance/return commands serialize on asset rows. Partial index holds(status,expires_at); UNIQUE org+serial. Expired holds keep active allocation until explicit transition; no volatile now() in index predicate. Repair quarantine can coexist with already committed future allocations only via unavailable asset flag; never insert overlapping maintenance row to bypass invariant.',
 'booking':'UNIQUE(org_id,quote_id,customer_id,operation_id) where operation identifier supplied; repeat same quote with new key may make distinct booking. versions BIGINT optimistic; INDEX(status,deadline_at) on sagas; UNIQUE(source_event_id) timeline within consumer. Quote snapshot immutable JSON validated contract. Cancel tombstone belongs saga/booking, survives terminal state.',
 'billing':'BIGINT money, nonnegative; captured<=authorized; refunded+reserved_pending_refunds<=captured. UNIQUE(org_id,booking_id) intent; UNIQUE(operation_id) ledger; UNIQUE provider_event_id. No ledger row mutation/delete; reversal new entry. PSP pending operation table required to persist amount reservation and outcome independently of network call.',
 'fulfillment':'UNIQUE(org_id,booking_id) job; UNIQUE(job_id) handover and return. booking_projection version monotonic; ownership queries index(org_id,depot_id,status). Return report amount nonnegative, condition enum, timestamps server-generated; serial list snapshot, opaque asset IDs.',
 'notification':'UNIQUE(org_id,subject_id,source_event_id) notifications; INDEX(subject_id,created_at,id) for SSE cursor; delivery UNIQUE(notification_id,channel), index(status,next_attempt_at); read_at TIMESTAMPTZ nullable. Never store full upstream booking payload if only title needed.'
}
for s in SERVICES:
    write(f"data/models/{s['id']}.md",f'''# {s['name']} logical data model

All id/org/subject references UUID unless OIDC subject opaque string; version BIGINT starts1; time TIMESTAMPTZ UTC. Business text length caps name120, reason1000, serial80. FK only within this database; org_id on every tenant-owned row. DB constraints supplement HTTP validation. Money integer BIGINT; JSON payload schema validated before persistence; no decimal floating point.

'''+'\n\n'.join(f"## {t}\n\nColumns: {cols}. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK." for t,cols in s['tables'].items())+f'''\n\n## Constraints / indexes / lifecycle

{MODEL_EXTRA[s['id']]}

Inbox/outbox/idempotency schema described in passport. Relational ER depicts cardinalities, not cross-service joins. Add created_at/updated_at where necessary in migrations; every mutable aggregate update checks version. Write migration forward, clean-install and upgrade-from-previous tests. No production seed fixture in migration. Query plan evidence: EXPLAIN ANALYZE on representative100k rows, record rows/read buffers and selected index; do not disable seqscan to force a desired result.
''')

TECHS = [
 ('Backend','Java21 + Spring Boot','Типизированные domain rules, transactions/security','Node/Nest, .NET, Go','JVM memory and library compatibility; pin Boot4.1 patch','HTTP lifecycle, DI, JDBC transaction boundary','M03 quote API and unit/integration suite','Explain rollback when exception is swallowed'),
 ('Backend','REST / OpenAPI','Явные HTTP contracts','gRPC/protobuf lab','No streaming optimization; breaking semantics need version','status codes, caching, deadlines, idempotency','M06 generated fixtures/provider checks','Explain why POST timeout does not mean failure'),
 ('Frontend','React / TypeScript','Accessible role-based UI and server-state handling','Vue/Svelte','UI types do not validate network at runtime','router, TanStack Query, forms, runtime validation','M11 checkout and operator E2E','Distinguish UI optimistic cache from booking authority'),
 ('Databases','PostgreSQL / Flyway','Owned durable aggregates and interval integrity','MySQL; ORM; Liquibase','Physical instance shared dev still has one failure domain','SQL, MVCC, locks, exclusion, plans, migration','M04 contention and query evidence','Explain write skew and why Redis lock is insufficient'),
 ('Caching','Redis','Bounded catalog cache and gateway throttling','in-process, HTTP ETag; no cache','Eviction and stale data; never inventory truth','TTL, memory max, noeviction vs allkeys-lru, persistence','M11 cache outage/rebuild lab','Prove stale cache cannot change quote price'),
 ('Messaging','RabbitMQ','Durable routed commands/events, DLQ','Kafka lab; Redis Streams; BullMQ','Queue topology and confirms need explicit ops','acks, confirms, routing, prefetch, quorum','M06 outbox/inbox crash replay','Explain confirm success without consumer business effect'),
 ('Messaging','Kafka comparative lab','Replayable depot utilization projection','RabbitMQ append-only event archive','Not installed core; partitions and rebalance costs','offsets, key ordering, retention, group rebalances','M14 comparative failure report','Explain ordering per key vs global ordering'),
 ('Security','Keycloak / OIDC','Authentication without home-made password flow','managed IdP; session BFF','IdP availability and token revocation semantics','PKCE, JWKS rotation, JWT audience, RBAC','M02 two tenants and revoke role','Explain authentication vs membership authorization'),
 ('Linux','Linux / DNS / TLS / Nginx','Runtime process/network and edge routing','Caddy, Traefik','Need operational skills, not host security changes here','users, signals, sockets, DNS, certificates','M01 lab and M15 network packet evidence','Explain DNS failure vs HTTP503 vs connection refused'),
 ('Containers','Docker / Compose','Repeatable local dependencies and images','Podman','Volumes consume disk; Compose not HA','layers, nonroot, networks, bind/volume, health','M01 immutable image and clean environment','Explain restart vs recreation vs lost volume'),
 ('Containers','Kubernetes / Helm','Independent deployments, probes and rollback','Compose on VM; Nomad','Cluster overhead; DB HA not supplied by StatefulSet','requests/limits, services, rollout, policies, storage','M15 kind/k3d deployment report','Explain readiness vs liveness with broker down'),
 ('Delivery','GitHub Actions','Repeatable changed-service checks and deploy','GitLab CI; Jenkins lab','Remote runner costs/permissions, local fallback scripts','DAG, caches, artifacts, OIDC, environment gates','M16 service-specific release and rollback','Explain why path filter can miss shared contract changes'),
 ('IaC','OpenTofu / Ansible','Cloud resource state + repeatable VM configuration','Terraform; cloud-native IaC','State secrets/lock, billing; Ansible not resource graph','plan/state/drift; idempotent playbooks','M17 sandbox plan and local VM convergence','Explain IaC state vs actual resources and second run'),
 ('Cloud','AWS optional sandbox','VPC/IAM/storage and cost reasoning','Azure/GCP; mandatory local equivalent','Real account optional and spending approval required','subnets, IAM, budgets, destroy, quotas','M17 local simulation or authorized sandbox report','Explain single VM production-like single failure point'),
 ('Observability','OpenTelemetry / Prometheus / Grafana / Loki / Tempo','Trace slow saga with metrics and logs','Jaeger, ELK','Storage/label cardinality cost; sampling changes visibility','trace context, histograms, exemplars, alerts','M12 diagnose poisoned event with correlation','Find trace across async edge without logging JWT'),
 ('Testing','JUnit / Testcontainers / Playwright / k6 / ZAP','Verify real transactions, UI, load and access attacks','Vitest, Gatling, Locust','Tests consume resources; synthetic fixture only','test levels, fault injection, percentiles, attack scope','M14 reproducible failure/performance evidence','Explain why 100% line coverage does not prove invariants'),
 ('System Design','ADRs / threat model / contract review','Document costs and reversible decisions','design review notes','Documentation must track actual change','ownership, consistency, recovery, architecture audit','M18 defend failure decisions','Explain where strong consistency ends and manual review begins')
]
dump('roadmaps/technologies.json',[dict(track=a,name=b,problem=c,alternatives=d,limits=e,learn=f,deliver=g,prove=h) for a,b,c,d,e,f,g,h in TECHS])
write('architecture/technology-decisions.md','# Technology map\n\nCore stack is selected, not everything listed is installed. Jenkins, gRPC, Kafka are comparative labs; service mesh, Redis Streams, BullMQ are evaluated alternatives, no mandatory installation. Version locks recorded by student M01; this pack includes no running backend.\n\n'+ '\n\n'.join(f'## {n}\n\n**Problem:** {p}. **Decision:** use in {t}. **Alternatives:** {a}. **Limits:** {l}.\n\n**Study:** {learn}. **Practice result:** {out}. **Understanding check:** {proof}.' for t,n,p,a,l,learn,out,proof in TECHS))

MILESTONES = [
 ('M01','Lab foundations','Linux, networking, Docker, Git','none','Build isolated lab; pin versions; seven empty service build boundaries; dependency Compose specification; no business implementation supplied','DNS/ports explained; clean machine instructions; each image independently builds','Kill local lab process; distinguish socket absence from health response','Architecture skeleton, version lock, resource inventory, environment README','One independent build per service; no shared DB role; dependency health evidence','Explain namespaces, loopback, TLS; show git diff and reproducible clean start','Lab footprint report; one nonroot image runs; documentation covers every command','Native image comparison with measured memory'),
 ('M02','Identity & tenant boundaries','OIDC, JWT, RBAC','M01','Integrate Keycloak PKCE; Tenancy memberships; owner checks on every endpoint; JWT never in localStorage','F01/N03 role matrix against two tenants; token audience/expiry tests','IdP/JWKS outage and revoked membership during form submit','Tenancy API, auth matrix, threat model baseline','401 invalid token;403 forbidden own command;404 foreign object; mutations revoke immediately','Explain issuer vs audience, authentication vs authorization','Role matrix automated; no cross-tenant cache/event leakage','BFF session comparison'),
 ('M03','Catalog & pricing','Java, REST, SQL, unit testing','M02','Catalog versioned rates, immutable quote, OpenAPI schema validation; integer money only','F02/F04 with25h/qty2 example and rate change','Catalog DB timeout during quote; ensure no booking created','Catalog image+migrations, price tests, fixture, API evidence','25h quote calculates10000 rental+20000 deposit; expired quote422','Explain rate snapshot and UTC/DST rounding','All quote bounds plus tenant tests pass; independent service build','gRPC quote lab benchmark'),
 ('M04','Inventory integrity','SQL locks/MVCC, PostgreSQL ranges','M03','Inventory own DB; asset/depot/maintenance models; atomic qty allocation; GiST overlap invariant; If-Match','F03/F13/F16 queries, conflict maintenance and asset lifecycle','Two concurrent holds/maintenance; DB deadlock abort/retry bounded','Inventory migration, ERD, contention report, query plans','100 simultaneous overlapping requests on one unit produce1hold; all-or-nothing qty5','Explain isolation and exclusion; inspect real constraints and plan','No overlapping active allocations; stale edit412; migration upgrade test','Serializable vs Read Committed contention experiment'),
 ('M05','Booking commands & idempotency','API operations, transactions','M04','Booking persists PENDING+outbox, durable request hash; acceptance202; owner lookup endpoint','F05/F07 same key same resource, mismatch409; clients poll pending','Response lost after DB commit; retry vs crash','Booking model/state tests, idempotency integration, UI pending draft','20 repeats create1booking; different tenant same key works','Explain 202 vs confirmed and persistence of response','Idempotency body hash and expiry/replay rules documented','Multiple-line booking design ADR'),
 ('M06','Messaging & contract gates','AMQP, event schemas, outbox/inbox','M05','RabbitMQ exchanges/queues/ACL; confirms+mandatory, ack after DB; AsyncAPI per service; contract fixtures','Reserve command→HoldCreated facts, delivery identifiers and version rules','Crash after confirm before mark, crash after commit before ACK, unroutable publish','Publisher/consumer tests, topology spec, fixture compatibility checks','At least10 duplicate deliveries yield one effect; poison schema→DLQ with original metadata','Explain confirms vs ack; no broker delivery equals transaction success','No lost committed outbox in induced crashes; publish/inbox metrics','Compare Redis Streams ownership/replay'),
 ('M07','Sandbox billing & confirmation saga','Saga, payment idempotency','M06','Billing sandbox adapter auth/query/void/capture/refund; Booking durable orchestration with deadlines','F06 successful auth+commit confirms; cost snapshot used','PSP succeeds then response lost; broker outage while hold expires','Billing models/ledger, saga transitions, sandbox fault controls','Unknown reconciled by same key; expired hold never committed; one auth','Trace confirmation; explain compensation not DB rollback','All forward/late event fixtures pass; no real money/card data','PSP circuit breaker experiment'),
 ('M08','Cancellation & races','Compensation, event ordering','M07','Cancellation tombstone, Inventory release idempotent, late auth void, deadline reconciliation worker','F08/F18 all partial states cancel; terminal does not resurrect','Cancel vs commit, reserve after release, late Authorized after Failed','Race tests with deterministic barrier; reconciliation runbook','100 runs each race: no cancelled active allocation/net captured; completion≤120s after recovery','Explain why timeout cannot mark cancellation complete','Race matrix and actual owner-state proofs retained','Property-based state machine exploration'),
 ('M09','Warehouse physical workflow','Fencing, frontend forms','M08','Fulfillment own jobs, projection+authoritative handover claim, all-assets return, damage quarantine','F09/F10 operator depot enforcement, serial inspection, overrun incident','Claim response lost; operator restart; return arrives before handover event','Warehouse API, handover/return UI, recovery incident scenario','Cancel/handover exactly one winner; double return one report; absent asset not handed over','Explain why handover claim has no automatic timeout release','Physical actions audited; no silent future reservation deletion','Partial return extension'),
 ('M10','Settlement & refunds','Financial invariants, reservations','M09','Capture≤auth; pending_refund reservation; immutable ledger; void remainder; manual review','F11/F12 late fee, damage, refunds and sandbox webhook signature','Capture succeeded then transport timeout; refund webhook duplicates and out-of-order','Ledger audit tests, refund UI, reconciliation operator evidence','15000 auth example yields8500 capture; two full refunds never overrefund','Explain pending refund vs recorded refund and available remainder','Ledger sums and provider outcomes agree for100 scripted cases','Deposit-only capture and progressive settlement'),
 ('M11','Product frontend & notifications','React, accessibility, Redis, SSE','M10','React typed routes/forms; server state; Notification TS own DB; Redis catalog cache; cursor SSE','F14/N09 keyboard flows, states, filters, pagination; notifications tenant-scoped','Redis down, SSE lost/reconnect, mail sink timeout','Implemented desktop/mobile UI, Playwright E2E, accessibility report, cache lab','360px no page overflow; duplicate fact one notification; fresh quote bypasses cache','Explain query cache vs business authority; keyboard demo','All core screen paths and loading/empty/error/denied states tested','Optimistic UI with explicit rollback'),
 ('M12','Observability & incident diagnosis','Tracing, metrics/logs, SLO','M11','OTel context over HTTP/AMQP; Prometheus histograms; Grafana dashboards; Loki logs; Tempo traces','F15/N05 correlate delayed saga with blocked adapter and queue age','Poison event, slow SQL, missing context on async hop','Dashboard JSON, alert rules, redacted incident report','Trace links across all saga edges; no high-cardinality booking metric label','Identify bottleneck from telemetry without reading implementation first','Reviewer diagnoses injected incident in15min with retained evidence','Tail sampling cost comparison'),
 ('M13','Contracts, migrations & CI','Compatibility, CI DAG, supply chain','M12','Provider/consumer fixtures, breaking diff gate, expand/contract migrations, image digest/SBOM scans','F17 backward-compatible optional field and independent build scripts','Shared schema change ignored by naive path filter; old consumer deployment','CI workflow, PR review, v1/v2 migration exercise','Old consumer passes additive schema; breaking change blocked; previous migration upgrade works','Explain enum evolution and meaning change that schema diff misses','CI executes real checks, not echo success; changed contract rebuilds impacted consumers','Jenkins pipeline comparison lab'),
 ('M14','Reliability & performance laboratory','k6, controlled fault injection','M13','Environment manifest, warmup/sample, trace/error denominators; retry/jitter/PSP breaker; DLQ replay; Kafka comparative projection','N01/N02/N04/N06 load thresholds and functional integrity under faults','120s broker outage, killed consumer after commit, partition, delayed PSP, poison payload','Raw load report, crash evidence, Kafka offsets/rebalance comparison','20VU read p95≤300ms command≤500ms saga≤5s healthy; recovery100 bookings≤120s','Explain percentile vs average, coordinated omission, recovery limits','Record failures and tuning impact; no fabricated charts/benchmark numbers','Stress until saturation, queue backpressure sizing'),
 ('M15','Production-like Kubernetes & security','Docker, networks, Kubernetes, Helm','M14','kind/k3d seven Deployments, own DBs, resource limits/probes, network policies, TLS; secrets nonrepo','N07 ingress only; DB denied to other owner; scale Inventory2 replicas respects invariant','Broker outage must not liveness-restart services; rolling update during hold','Helm charts, measured resources, threat tests, topology capture','Old pods drain30s; own migration job; wrong DB role denied; rollout maintains invariants','Explain StatefulSet is not HA, PVC/backups, readiness gates','Clean local cluster deploy and security matrix pass; lab overhead recorded','Three-node quorum broker fault lab'),
 ('M16','Independent delivery & rollback','CI/CD, rollout, signed digest','M15','Deploy per-service digest after smoke/contract/migration checks; environment gate; previous image retention','F19 release Notification without six core image changes','Bad readiness image, incompatible required field, failed migration','Release pipeline and rollback evidence with before/after digests','Notification-only diff; failed update leaves working pods; revert image retains schema compatibility','Explain why destructive migration cannot be rolled back by image rollback','Actual release/rollback recorded, previous consumer works expanded schema','Canary traffic and automated rollback thresholds'),
 ('M17','IaC, backup & restore','OpenTofu, Ansible, storage/reconciliation','M16','Mandatory local isolated VM/state simulation; optional AWS sandbox only after user spending authorization; snapshots, encryption and restore','F20/N10 isolated restore; state/provider reconcile across differing backup cuts','Missing volume, corrupt backup, mismatched service restore points','IaC plan, idempotent Ansible report, backup inventory, timed restore','Second Ansible run unchanged; restore≤30min fixture, delta known; no credentials in state repo','Explain resource graph, drift and RPO vs RTO; estimate cloud cost with sourced assumptions','Clean recovery proves allocation/ledger counts and reports unrecoverable delta','PITR coordinated recovery watermark'),
 ('M18','Engineering audit & architecture defense','All prior evidence','M17','Clean install, demo every core journey, independent release, security/resilience/performance/restore, architecture questions','All F01–F20 and N01–N12 have verified evidence and reviewer verdict','Reviewer chooses unexpected fault; no coaching during diagnosis','Audit report, demo script, coverage ledger, final ADR updates','Every requirement evidence link resolves; reviewer independently runs critical races/recovery','Defend every boundary; explain smaller commercial alternative and current trade-offs','No open integrity/security blockers; unresolved limitations explicit; not merely all task checkboxes','Interview presentation with measured evidence')
]
milestones=[]
for mid,title,learn,pre,tech,fun,fault,deliver,ac,review,dod,bonus in MILESTONES:
    ids=[s['id'] for s in stories if s['milestone']==mid]+[i for i,t,a,m in NFR if m==mid]
    milestones.append(dict(id=mid,title=title,skills=learn,depends=[] if pre=='none' else [pre],requirements=ids,acceptance=ac))
    write(f'assignments/{mid}.md',f'''# {mid} — {title}

## Title / Context
{title}. Самостоятельный инженерный этап DepotFlow. Ценность в реальной работе: {fun}. Ориентир трудоёмкости 15–40 focussed sessions по1–3h (архитектура/restore может больше); это planning assumption, не обязательный срок и не обещание результата.

## Learning Objectives
{learn}. Уметь объяснить причину выбранного механизма, альтернативу и ограничение до реализации.

## Prerequisites
{pre}. Прочитать product/business-processes.md и соответствующие service passports/контракты. Перед практикой объяснить незнакомые термины; не копировать готовое бизнес-решение.

## Technical Requirements
{tech}.

## Functional Requirements
{fun}. Связанные требования: {', '.join(ids) or 'A03/A05 platform acceptance'}.

## Constraints
Семь независимых владельцев данных; никакого shared database access или подмены backend+worker. Бизнес-код пишет студент. Все retries ограничены, деньги integer, состояния durable, tenant checks server-side. Только sandbox, синтетические данные, isolated lab. Не менять личные VM/credentials/main/remote для выполнения учебного этапа.

## Expected Deliverables
{deliver}. Дополнительно: README воспроизведения с местом запуска каждой команды и смыслом аргументов, evidence/{mid}/manifest.json (commit, image digests, CPU/RAM, dataset seed, UTC time), raw test outputs, ADR если изменились границы.

## Acceptance Criteria
{ac}.

Для каждого связанного F/N требования повторить соответствующий Given/When/Then. Показать независимый запуск теста и состояние после операции, не только HTTP response. Результат = pass/failed/blocked с ссылкой на evidence; непроверенное не pass.

## Testing Scenarios
Positive: {fun}. Negative: forbidden tenant/role, malformed body, unavailable required owner, conflicting operation. Boundary: zero/one/max qty, exact expiry and interval endpoints where relevant. Запустить unique-key повтор и stale version; fixtures в reviews/scenarios.json. Unit tests не заменяют DB/transport experiments.

## Failure Scenarios
{fault}. Записать trigger → observed state → recovery → invariant checks. Рестарт контейнера должен сохранять committed state. Отказ воспроизводится в изолированной среде без удаления чужих данных.

## Review / Audit
{review}. Reviewer выбирает один негативный сценарий сам, читает transaction boundary, проверяет ownership credentials и контракт. Нельзя пройти этап только по screenshot/green checkbox.

## Definition of Done
{dod}. Deliverables доступны, acceptance evidence со стабильными IDs, review замечания resolved или explicit limitation, clean-start инструкции повторены. Правила Ready/Done в operations/engineering-process.md.

## Bonus / Advanced
{bonus}. Bonus после обязательных проверок; записать ADR и сравнение, не добавлять инструмент без сценария.
''')
dump('assignments/milestones.json', milestones)

TRACKS = [
 ('Project',['M01','M04','M08','M11','M14','M18'],['Изолированная среда','Целостность ресурсов','Saga компенсации','Полный интерфейс','Отказная лаборатория','Защита']),
 ('Backend Engineering',['M01','M03','M05','M07'],['HTTP/JVM fundamentals','Неизменяемая котировка','Durable commands','Saga + sandbox adapter']),
 ('Frontend Engineering',['M02','M05','M09','M11'],['Auth/access routes','Pending server state','Warehouse forms','Accessible E2E']),
 ('Databases',['M03','M04','M10','M17'],['Модель/migration','Locks & plans','Ledger invariants','Restore verification']),
 ('Distributed Systems',['M05','M06','M08','M14'],['Operation identity','Outbox/inbox','Compensation races','Fault evidence']),
 ('Redis & Caching',['M03','M11','M14','M15'],['Authoritative quote first','Cache-aside + invalidation','Eviction/outage experiment','Bounded production config']),
 ('Message Brokers',['M05','M06','M08','M14'],['Contracts','Rabbit confirms/ack','Late events + DLQ','Kafka compare/rebalance']),
 ('Linux & Networking',['M01','M02','M12','M15'],['Processes/sockets/DNS','TLS/auth','Trace network failure','Network policies']),
 ('Docker & Kubernetes',['M01','M13','M15','M16'],['Images/volumes','Independent builds','Probes/limits','Rollout/rollback']),
 ('CI-CD & IaC',['M01','M13','M16','M17'],['Git/reproducibility','Check DAG','Per-service release','State/drift/convergence']),
 ('Cloud',['M01','M15','M17','M18'],['Local environment baseline','Trust/network topology','Plan/budget or local equivalent','Defend failure domain']),
 ('Observability',['M05','M06','M12','M14'],['Correlation IDs','Async trace context','Dashboards/alerts','Incident & SLO evidence']),
 ('Security',['M02','M10','M13','M15'],['Tenant/role controls','Signed webhooks','Dependency/supply chain','TLS/network attacks']),
 ('Testing Performance Reliability',['M03','M06','M14','M17'],['Pure vs integration','Contract/crash testing','Load+fault experiments','Timed recovery']),
 ('System Design',['M01','M04','M08','M18'],['Boundaries & ADR','Strong local invariants','Eventual consistency costs','Architecture defense'])
]
tracks=[]
for name,steps,labels in TRACKS:
    slug=re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')
    nodes=[]
    for mid,label in zip(steps,labels):
        mm=next(x for x in milestones if x['id']==mid)
        nodes.append(dict(milestone=mid,label=label,practice=mm['title'],proof=mm['acceptance'],depends=mm['depends']))
    tracks.append(dict(name=name,slug=slug,nodes=nodes))
    write(f'roadmaps/{slug}.md',f'# {name} roadmap\n\nПоследовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.\n\n'+'\n\n'.join(f"## {j+1}. {n['label']} — {n['milestone']}\n\nPrerequisite: {', '.join(n['depends']) or 'none'}.\n\nПрактика: {n['practice']}. Evidence: {n['proof']}.\n\nПроверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/{n['milestone']}.md)." for j,n in enumerate(nodes)))
dump('roadmaps/tracks.json', tracks)

ADRS = [
 ('001','Seven bounded services and monorepo','Accepted','Owner boundaries reflect money, physical assets and irreversible warehouse action. Monorepo makes contract review discoverable while own builds/releases prevent deployment coupling.','Single small commercial team might choose monolith; goal here explicitly distributed practice. Separate repos increase workflow costs.','Proof F19 separate digests and DB grant denial; reconsider Notification split if ownership costs exceed benefit.'),
 ('002','RabbitMQ plus durable outbox/inbox','Accepted','Command routing and modest volume fit queues. Persist domain+outbox atomically and consume inbox+effects transactionally.','Kafka offers retained log/replay but partition/offset complexity is unnecessary core; no exactly-once promise.','Kill publisher and consumer at boundaries; preserve stable IDs, ACK after commit.'),
 ('003','Inventory temporal exclusion','Accepted','Allocation correctness belongs a single SQL transaction and owned database, including maintenance blocks.','App-only check races; Redis locks can expire and split ownership. SQL lock contention is real cost.','100 simultaneous overlaps and repair races; observe GiST exclusion and row locks.'),
 ('004','Durable orchestration and compensation','Accepted','Booking saga makes deadlines and recovery visible; no cross-database transactions.','Choreography reduces central coordinator but hides cancel/late auth handling. Manual review remains for irreversible physical steps.','Cancel/commit, hold expiry and late auth matrices; reconcile unknown PSP.'),
 ('005','REST first, no core gRPC','Accepted','Human-readable contracts and troubleshooting outweigh unmeasured throughput benefit.','gRPC comparative lab permitted, generated clients and transport debugging add complexity.','Measure same availability query in lab and record decision, no artificial polyglot sprawl.'),
 ('006','Keycloak authentication and Tenancy authorization','Accepted','OIDC avoids bespoke password system, authoritative membership protects business commands.','Gateway-only auth insufficient; JWT role revocation stale. Lookup availability reduces write availability.','Role revocation after open form prevents mutation; fail closed Tenancy down.'),
 ('007','Compose first, Kubernetes final lab','Accepted','Sequential implementation keeps seven-service target while deferring scheduler overhead until integrity proven.','Kubernetes needed for final deployment exercise, not a proof of reliability; one-node cluster remains single failure domain.','Probe/rollback, DB restore and own network grants must be tested.'),
 ('008','Redis outside correctness path','Accepted','Cache model lists60s, compute quotes from authoritative rates.','Cache invalidation and eviction add failure states; a small dataset may not need cache commercially.','Outage leaves pricing/allocation unchanged, measure SQL load and cache hit rate.'),
 ('009','Handover fencing','Accepted','Booking atomically claims handover before irreversible physical transfer; cancellation loses after claim.','Claim can strand without physical act; no automatic expiry safe in presence of lost response.','Manual review explicitly checks warehouse act and never silently releases possibly rented asset.'),
 ('010','Local-first cloud practice','Accepted','All mandatory work runnable local; IaC concepts learned in isolated VM/provider simulation, AWS optional.','Simulation does not prove real IAM/network or managed cloud behavior; cloud-specific claims need authorized sandbox evidence.','Audit labels local vs live, includes cost assumptions and destroy evidence if sandbox used.')
]
for i,title,status,decision,trade,proof in ADRS:
    write(f'architecture/adrs/ADR-{i}.md',f'# ADR-{i}: {title}\n\nStatus: {status}; date 2026-10-11; assignment design baseline.\n\n## Context / decision\n\n{decision}\n\n## Alternatives / consequences\n\n{trade}\n\n## Verification / reconsideration trigger\n\n{proof}\n\nImplementation may supersede this decision only with a new ADR preserving required learning outcomes and updating contracts, diagrams, task evidence and coverage. No undocumented deviation.')

write('operations/environments.md', '''# Environment and deployment specification

These are target designs; nothing provisioned by this assignment pack. Windows edits/viewing; Linux lab (WSL2 or isolated VM) is where future Docker/Kubernetes commands run. Do not modify current personal VMs or system settings without approval. Student measures available CPU/RAM first.

| Profile | Budget assumption | Topology | Purpose / limitation |
|---|---|---|---|
| lab-lite |4vCPU,8GB,20GB free|Compose subsets, JVM Xmx192m initially, DB instance separate owned DBs|First milestones; no full stack SLA benchmark|
| lab-standard |8vCPU,16GB,40GB free|7services, own DBs one Postgres node,1Rabbit,1Redis,Keycloak, telemetry|Fixed N01 load and restore fixture, no HA|
| lab-cluster |8vCPU,24GB,60GB free|kind/k3d3nodes, replicas2 core where needed,3Rabbit quorum, own DB credentials|Failure experiments; nodes share host failure domain|
| production-like |Same cluster or isolated VM|TLS, independent images, migration jobs, policies, backup target separate volume|Demonstrate operations; no production uptime claim|
| optional AWS |User authorized sandbox budget only|VPC private subnets, ingress VM/load balancer, storage, IAM, budget alarm|Live cloud requires measured cost/cleanup; not performed by author|

Requests starting values per JVM cpu100m/memory256Mi, limits cpu1/memory512Mi; Node100m/128Mi to1/256Mi. These values must be profiled, not assumed stable for chosen framework. DB/Rabbit/Keycloak needs separate limits and volume budgets; resource sum recorded, OOMKilled evidence changes settings. Startup probe every5s up to120s; readiness DB/pool every5s with3fail; liveness process every10s with3fail. Broker fault must not restart entire fleet. terminationGracePeriod30s, preStop stops command acceptance/consumers then drains transaction≤20s. pdb minAvailable1 only with2 replicas, not magic protection for one pod.

Ingress443 only; internal HTTP8080 over TLS production-like. Own DB5432, broker5671, Redis6379 TLS as supported/configured, OTel4317; admin ports only loopback in dev. Default deny in cluster, explicit connection matrix operations/network-security.md. Keycloak persisted independently, never share service DB users. Migrations per owner init/job before rollout; conflicting migration workers serialized. Persistent volumes require backups; StatefulSet doesn't supply DB replication automatically.

Compose design: networks edge, app, data, telemetry; only gateway connects edge/app, service joins app+own data, expose no DB/broker publicly. Compose networks not a strong per-service firewall; DB grants and OS/cluster policy provide real denial tests. Compose manifest is student deliverable M01; no pretend deploy YAML with missing application images shipped here.
''')
write('operations/network-security.md', '''# Allowed connections / threat model

| Caller | Destination | Protocol | Authorization |
|---|---|---|---|
| Browser | gateway / IdP |HTTPS443|PKCE, user access token in memory; CSP, strict CORS, no secrets in browser|
| gateway |7HTTP services|HTTPS internal|JWT forwarded; gateway strips spoofed X-Org/X-User|
| every service |Tenancy membership, Keycloak JWKS|HTTPS|scoped service identity + original subject; issuer/audience validated|
| Booking |Catalog quote lookup, Inventory/Billing status|HTTPS|booking service scope plus tenant|
| Fulfillment |Booking claim/status|HTTPS|fulfillment scope plus operator/depot|
| Tenancy |Inventory depot lookup|HTTPS|tenancy scope plus org|
| each service |own Postgres only|TLS5432|own app role; DDL migration role separate|
| event services |RabbitMQ|AMQPS5671|per-service ACL, commands address owner|
| Catalog/gateway |Redis|TLS6379|named ACL prefixes; no auth source|
| Billing |sandbox PSP|HTTPS|secret, provider idempotency key, signed callbacks|
| Notification |mail sink|SMTP internal|synthetic recipient; stable Message-ID|
| services |OTel collector|gRPC/HTTPS4317|internal identity; PII filter|
| collectors |Prometheus/Loki/Tempo|internal|no public dashboards without operator auth|

Default deny elsewhere. No cross-owner SQL, no direct client DB/broker, no management ingress on public network. TLS cert rotation exercise; service credentials have distinct audiences/scopes and network source alone does not authorize command.

Threats and tests: object authorization(IDOR)→two-tenant endpoint/event/SSE suite N03; role revocation→authoritative command check F01; forged tenant headers→gateway strip plus server derivation; forged PSP callback→HMAC timestamp within5min constant-time verification, unique provider_event_id; replay older signed callback→idempotency not duplicate money; SSRF→no user-controlled outbound URL; SQLi→parameterized queries; XSS→text output and CSP, no unsafe HTML user content; log leakage→scan token-like fixtures; resource exhaustion→body max64KB, per-org rate limits (20read/s,5command/s baseline), bounded thread/consumer pools; dependency attack→lockfile/SBOM/scan and signature/digest review.

TLS certificates/secrets in mounted file or secret store, not ConfigMap; rotate one principal at time with overlap, prove old revoked. Access token short-lived5min, no JWT/email in localStorage/logs. Frontend runtime auth remains memory; refresh via secure approach documented by student (BFF HttpOnly SameSite or IdP flow); prototype uses no authentication and is labeled as demonstration. Minimal synthetic data retention N11; legal compliance of a real business is out of scope, not asserted.
''')
write('operations/engineering-process.md', '''# Engineering process / onboarding

Monorepo target: apps/web, services/{tenancy,catalog,inventory,booking,billing,fulfillment,notification}, contracts, platform/{compose,helm,iac,ansible}, docs, tests/{contract,e2e,load,resilience}, evidence. This pack is specification only; student creates implementation repository separately. No Git initialization/commit/push performed here.

Small trunk-based changes on codex/<topic> (or team convention), PR to protected main, no direct main writes. Feature flag incomplete behavior; each PR one explainable risk. Commit reviewed by student, no automatic commit/push by tutor. Independent semantic image tag + immutable digest per service, package source commit recorded.

Coding: strict TS, no any to bypass network validation; Java explicit aggregate boundaries and constructor dependencies; controller validates transport, domain enforces invariants, repository owns SQL; never call PSP under long DB transaction. Formatting automated per language, meaningful tests for invariants. Money utility immutable, no duplicated arithmetic assumptions. Error codes stable; logs JSON, no tokens. Graceful shutdown/health per passport.

Definition of Ready: requirement ID and intent, contract/state impact, fixtures, negative/failure acceptance, known dependencies, reviewable scope. Definition of Done: code + own migration + contract review + positive/negative/failure evidence + docs/diagram updates + clean-start + reviewer approval + known limitation entry. Coverage percentage/checkbox alone not Done.

PR checklist: ownership intact? who can call? race proof? operation key stable? timeout unknown? outbox/inbox transaction boundaries? retry bounded? schema old reader compatibility? resource/log/security impact? deployment/rollback and migration evidence? Student must explain without generated answer memorization.

Backlog epics: E01 Identity/catalog M01–M03; E02 Inventory/booking M04–M05; E03 Delivery/saga M06–M08; E04 Warehouse/finance M09–M10; E05 UI/telemetry M11–M12; E06 Reliability/platform M13–M17; E07 Audit M18. Stories F01–F20 map to milestones; each milestone splits tasks: design contract, implement owner, validate negative/fault, reviewer evidence. Tasks have unique <Mxx>-T01..T04, no generic done flag without tests.

Contract review: proposed change, old/new examples, semantics/authorization, impacted consumers, compatibility fixture gate. Optional fields are additive only if old reader ignores unknown fields; new enum values may break generated exhaustive clients -> deploy tolerant reader first. Breaking event type new major, coexist ≥two releases, do not delete v1 until all consumers upgraded and DLQ/history migration decided. Data migrations expand(add nullable/new table)→dual write/backfill measured idempotently→switch reader→contract later release; backward compatible rollback uses old image with expanded schema. No drop/rename in same release.

Onboarding: read README/PRD, run dependency checks in isolated lab, compare ER/contract to story, implement M01 then follow DAG; explain each shell command before using it. Tutor sequence: explanation → independent practice → inspect evidence → error analysis → skill confirmation. If implementation is requested later, don't supply full solution unless user explicitly asks. Keep evidence raw; failed experiment teaches more than guessed success.
''')
write('operations/release-rollback.md', '''# Release and rollback runbook

Owner: implementing engineer; reviewer verifies evidence. Trigger: per-service change with tests and contract compatibility accepted. Record environment, previous and new digest, migration version, UTC start, operator, backup checkpoint. Precheck previous consumer runs expanded schema, image SBOM scan no untriaged critical issues, essential secrets mounted, no destructive migration. Migration job completes once for owner; failure halts rollout and preserves previous image.

Deploy one service digest. Check readiness and smoke commands through gateway with synthetic org; examine eligible error rate, queue age, saga latency for5min at fixed workload. Threshold trigger: readiness unavailable>60s OR eligible errors>5% for2min OR integrity failure any count. Halt and restore previous image digest; do not undo compatible expand migration. Drain new pods; confirm old replica healthy, retry stable operation IDs, inspect unknown provider ops. Reconcile in-flight saga before declaring recovery. Record actual metrics and owner states.

If data corruption or incompatible destructive migration already occurred: stop mutations, preserve logs/volumes, incident lead decides restore+reconcile from isolated backup; simple image rollback cannot fix data. Never auto replay charge with new key. Release checklist: tests/contract/scan evidence, migration compatibility, artifact digest, deploy scope, smoke, observation, rollback ready, docs updated. Notification-only release must leave six business service digests identical F19.
''')
write('operations/backup-recovery.md', '''# Backup & recovery plan

Target N10: snapshot RPO≤24h, fixture measured RTO≤30min; no monthly production guarantee. Back up each owned DB including inbox/outbox/saga/idempotency and Billing pending operations, Keycloak config/store, broker topology definitions, version manifest. Broker queue snapshot alone insufficient for domain recovery; outbox is durable source. Redis cache rebuilds, not backed up for correctness. Store encrypted artifacts on independent lab volume, checksum and restore-test; 7daily+4weekly retention assumption. Credentials outside backup report, authorized only.

Consistent cut workflow: stop incoming mutation acceptance, let current transactions drain, record global maintenance watermark and per-owner DB snapshot time/WAL position; snapshot all owners and topology; release traffic after checkpoints saved. An advanced live-backup exercise uses unequal cut times and must reconcile, not pretend global atomicity.

Restore isolated namespace from manifest, verify checksums, own DB grants and schema, keep consumers/external delivery disabled. Run invariant queries via owner's audit interface: overlap0, captured/refunded bounds, counts at checkpoint, saga phase correlation. Compare PSP sandbox operations by stable key; snapshot may predate successful charge. Reconcile pending intents before consumers on, then resume outbox/inbox preserving IDs. External email may duplicate after old snapshot — report. Rescan terminal compensation and future unavailable asset jobs. Do not restore directly over running original environment.

Evidence: UTC downtime start/end, bytes/counts per owner, chosen snapshot and actual delta, failed restore attempt if any, measured RTO/RPO, recovered IDs, sandbox ledger reconciliation, release of mutation traffic. Missing/corrupt backup is failure; do not declare recovery based on container health. Exercise delete only explicitly named isolated test volume with verified path/namespace, never personal VMs or original data.
''')
RUNBOOKS = [
 ('stuck-saga','saga_pending_seconds>60','Find correlation in Booking timeline, trace Inventory/Billing commands and outbox age; query authoritative owner status by booking_id/provider_key.','If provider UNKNOWN query sandbox before any retry. Requeue original valid command ID after dependency healthy; never manual-set CONFIRMED.','After recovery100 bookings finish or explicit manual_review within120s; no cancelled allocation/net captured. Escalate ambiguous handover to physical check.'),
 ('dlq-replay','DLQ count>0','Read schema error, consumer version, retry history; distinguish poison payload from outage. Preserve original event and metadata.','Fix compatible consumer or quarantine invalid schema. Replay one valid message original event_id, monitor then batch max20. Never generate fresh identity to bypass inbox.','Inbox+effects single commit; no duplicate ledger/allocation; poison remains documented with owner.'),
 ('broker-outage','broker unavailable / oldest outbox>60s','Check socket/DNS/TLS/ACL and confirms; inspect outbox/inbox; healthy HTTP acceptance may leave pending.','Restore broker/topology, bounded backoff workers; publisher mandatory route confirms before marking. Scale consumers only after observing DB capacity.','Drain backlog to0; compare all outbox effects, pending ages and deadline compensations; no mass pod restarts.'),
 ('payment-unknown','payment_unknown_total>0','Lookup intent operation and provider_key; inspect signed webhook history and trace masked transport error.','Query provider exact same key; persist capture/void/refund independently. Missing response is not decline. Manual review if provider result irreconcilable.','Provider net and ledger net match; total captured≤auth and refund≤capture incl pending; no new charge key.'),
 ('asset-overrun','past-end IN_USE / asset.unavailable','Check physical handover, scheduled end, return report and future commitments; identify impacted depots/bookings.','Mark asset unavailable and block handover, notify dispatcher. Resolve manually with cancel+compensation or documented advanced replacement; do not erase future allocations.','Every impacted job has blocked/compensated or substituted evidence; no absent asset handed over.'),
 ('slow-api','p95/error budget target exceeded','Trace gateway→Tenancy→owner DB, compare histogram and SQL buffers, queue/thread pool wait; inspect resource limits.','Remove accidental N+1 or missing index after measured query plan; set bounded pool/backpressure. Roll back regression image if threshold release gate met.','Repeat same seed/workload/hardware, publish before/after and error denominator; do not average p95 values.'),
 ('credential-rotation','expired TLS / scheduled principal rotation','Find scope affected, expiry, mounted version; redact secrets from report.','Create overlap credential, roll one caller, verify new access; revoke old; ensure own DB/broker grants preserved. Lab principal only.','New accepted old rejected, no expanded privileges, app healthy; audit owner/time with no secret values.')
]
for slug,trigger,diag,recover,verify in RUNBOOKS:
    write(f'operations/runbooks/{slug}.md',f'# Runbook: {slug}\n\n## Trigger / owner\n\n{trigger}; implementing engineer, warehouse operator where physical action involved. Lab only.\n\n## Diagnosis\n\n{diag}\n\n## Recovery\n\n{recover}\n\n## Verification / escalation\n\n{verify}\n\nCapture correlation, state snapshots from owners, UTC times and exact induced fault. If unverifiable leave incident open. See incident template; no force SQL status change across owners.')

write('reviews/test-strategy.md', '''# Test strategy and benchmark methodology

Unit tests pure pricing/state rules fast per service; Integration real Postgres/Rabbit/Redis with Testcontainers includes lock contention and ack/confirm boundaries; contracts old consumer/provider fixtures; E2E gateway/UI synthetic tenants; security auth/input/outbound cases; resilience deterministic hooks/barriers at transaction boundaries; k6 load healthy vs degraded. No minimum line-coverage number masquerades as correctness. Critical invariants and transitions must each have at least one counterexample test and positive proof.

Fixture seed20261011: org A/B; depots Tallinn/Tartu; model drill (€25/day,€100deposit), qty1 scarce asset, qty5 pool, damaged and maintenance assets; customer Alice/Bob, operator Tallinn/Tartu, finance/admin. Money amounts synthetic. Dataset baseline100 models,1000assets,10000bookings; query-plan lab100k rows separate from N01 baseline. Clocks configurable injected UTC; simulation now2026-11-02T08:00:00Z; production uses DB clock.

N01 benchmark lab-standard manifest: CPU/RAM, OS/runtime/image versions, load generator separate process, no internet PSP, fixed seed/dataset, warmup2min, steady10min20VU, mixed workload70% read20% checkout/cancel10% warehouse/finance scripted valid steps. Measure API acceptance separately from saga completed, error denominator eligible requests excludes deliberate409/422/auth failures but includes dependency5xx. Export raw samples, count/errors, p50/p95/p99, histogram, resources/queue age. Three runs report each and variability, no fictional averages. Healthy saga p95≤5s; deadline10min not performance success. Stress grows load5VU steps until saturation; results measured, no target user count beyond baseline.

Faults: Rabbit unreachable120s, kill consumer after DB commit beforeACK, outbox publisher after confirm, PSP outcome response lost, invalid webhook, Redis eviction/down, DB lock timeout/deadlock, slow Tenancy, late/out-of-order events, pod rollout, missing volume in isolated restore. Record invariant before/during/after, recovery time and pending states. Acceptance comparisons always same hardware/workload, and architecture claims limited to experiment. Scan security only explicitly lab URLs, never public employers/sites.

Commands are future implementation convention, **not existing runnable business tests in this pack**: ./mvnw -pl services/inventory verify (Linux repo root; -pl selects module, verify executes test lifecycle); npm run test:e2e -- --project=chromium (web repo; Playwright project); k6 run -e BASE_URL=https://lab.local tests/load/checkout.js (-e sets lab target); kubectl rollout status deployment/booking -n depotflow (-- namespace selects isolated lab). Student creates these entrypoints and documents local tool version/arguments at each milestone. Avoid scripts that return0 without executing assertions. Actual pack verifier is tools/verify_pack.py.
''')
SCENARIOS = [
 dict(id='SC01',requirements=['F04'],setup='rate2500 deposit10000 qty2 duration25h',action='create quote',expect='rental10000 deposit20000 auth30000'),
 dict(id='SC02',requirements=['F05','N02'],setup='one ready asset, shared interval,100 distinct keys',action='barrier starts100 checkout commands',expect='one active hold/allocation;99rejected;no overlap'),
 dict(id='SC03',requirements=['F06','F18','N04'],setup='authorized response delayed until after hold expiry',action='expire then deliver Authorized twice',expect='no confirmation;one void;allocation inactive'),
 dict(id='SC04',requirements=['F08','F09'],setup='confirmed booking same version',action='concurrent cancel and handover claim',expect='one winner;cancel winner no handover;claim winner cancel409'),
 dict(id='SC05',requirements=['F12'],setup='captured8500 refunded0',action='two simultaneous refund8500',expect='one reserved/succeeded;sum refunds<=8500'),
 dict(id='SC06',requirements=['F01','N03'],setup='tenantA token tenantB booking',action='GET/cancel and SSE subscribe foreign',expect='404 no PII;no mutation/event leakage'),
 dict(id='SC07',requirements=['F10','F13'],setup='return damaged with future allocation',action='return then try future handover',expect='quarantine/unavailable;incident;no silent allocation removal'),
 dict(id='SC08',requirements=['F07'],setup='persisted booking, response lost',action='20 repeats same key/body;then changed body',expect='same ID20times;409mismatch changed'),
 dict(id='SC09',requirements=['F18','N04'],setup='consumer committed business+inbox notACK',action='kill/restart/receive again',expect='one effect,ACK replay;no missing outbox'),
 dict(id='SC10',requirements=['F20','N10'],setup='maintenance cut manifest+snapshots',action='isolated restore+reconcile',expect='counts/invariants match;actualRTO/RPOreported'),
 dict(id='SC11',requirements=['F03','F14','N09'],setup='26models, keyboard only,360px',action='filter/page checkout, pending update, return',expect='no page overflow;focus/errors announced;cursor no duplicates'),
 dict(id='SC12',requirements=['F17','F19','N08'],setup='old consumers deployed;expand schema',action='add optionalfield then Notification-onlyrelease/rollback',expect='oldcompatible;six unchangeddigests;rollbackwithoutDBloss')
]
dump('reviews/scenarios.json',SCENARIOS)
dump('data/fixtures.json',dict(seed=20261011,clock='2026-11-02T08:00:00Z',organizations=['org-A','org-B'],depots=['Tallinn','Tartu'],models=[dict(name='Cordless drill',daily_minor=2500,deposit_minor=10000,currency='EUR')],assets=['scarce-001','pool-001','pool-002','pool-003','pool-004','pool-005','damaged-001'],roles=['customer','operator','finance','org_admin'],note='Symbolic fixture IDs must be replaced with UUIDs by test factory; no real user data'))
write('reviews/reviewer-guide.md', '''# Reviewer guide

Do not accept a feature solely because endpoint returns200. Check owner state, actual foreign-data denial, stable retry identity and independent artifact. Every milestone has reviewer questions; answers deliberately not supplied so student must reason. Ask transaction boundary: what happened if crash one instruction earlier/later? Which state could be unknown? Who owns correction? What proof supports the claim?

Typical errors: shared ORM tables masquerade as microservices; gateway auth only; availability query used as final lock; preACK before DB commit; outbox row marked before confirm; discard every low-version event and miss late auth void; Redis expiry mistaken for business release; cancelling handover claim on TTL despite physical action; generated enum rejects additive event; image rollback after schema drop; source token in trace; pod readiness cited as restore proof.

Technical probes: contrast Read Committed and serializable write skew; show range constraint; explain PSP response-loss and provider key; explain duplicate business effect vs external email; draw consumer transaction; trace wrong tenant header; debug partial restore; explain p95/error denominator; show an actual independent Notification deploy with six unchanged images. Change requirements mid-review: partial return, multi-currency, depot transfer, rate update during quote, provider authorization expiry. Ask student which contract/state/ADR/migration changes first and which old consumer still runs.

Grading: pass only when reproducible evidence meets all required criteria; failed integrity/security blocks stage. Performance miss requires profile/tune or explicit reviewer-approved environment adjustment with rerun; no silent lowered threshold. Optional tasks never compensate for missing core. Review record requires requirement ID, evidence path, reviewer, date, verdict and limitation.
''')
write('reviews/engineering-audit.md', '''# Final Engineering Audit — M18

Audit packet: commit/digests, exact lab profile, coverage ledger, contracts, ADRs, environment manifest and raw tests. Independent reviewer executes; this assignment pack has not run the future business tests. Mandatory gates below are all required, not points averaged into pass.

| Gate | Scenario | Pass evidence |
|---|---|---|
| A01 Product |quote→confirmed→handover→damaged return→settle→refund plus cancel|F01–F16 endpoint/UI/state evidence; exact money example|
| A02 Integrity |100reserve contenders, cancel/claim, duplicate/refund,lateauth|N02 zero invalid allocations/money changes; deterministic repeat100times|
| A03 Microservices |own DB grants,builds,images,migrations,contracts|seven independent business boundaries; foreign SQL denies; F19 release scopes|
| A04 Sync/async |quote GET and claim; AMQP reserve/facts|trace and broker effects; outbox/inbox crash recovery|
| A05 Delivery |additive contract, old consumer, roll/rollback|F17/F19 CI real assertions; expanded schema rollback|
| A06 Security |two tenants,role revoke,invalid token/webhook,policy denial|N03/N07 no cross-owner data/credentials|
| A07 Reliability |broker120s,PSPunknown,poison DLQ,missing contexts|N04/N05 recover within target or visible manualreview; no invented success|
| A08 Performance |fixed 20VU workload,3runs,raw samples|N01/N06 measured thresholds and eligible error denominator|
| A09 Recovery |isolated backup restore+PSPreconcile|N10 measured RTO≤30min/RPO≤24h and known checkpoint counts|
| A10 Reproducibility |fresh lab install,role UIs keyboard360px|N09/N12 clean start and no mandatory cloud/CDN|
| A11 Defense |random fault diagnosis≤15min, ownership trade-offs|student explains decisions,limitations and response-loss ambiguity|

Demo (~60–90min planning assumption):10min topology/ownership,15min core business,15min races/faults,10min release/restore summary then independent replay,15min troubleshooting and security,15min design questions. Full load/restore may run outside demo but raw evidence must be reproducible. Reviewer picks at least one fault not disclosed in advance. Code inspection focuses locks, inbox/outbox commit, provider adapter and authorization, not formatting.

Final verdict: ACCEPTED only all gates pass and no open integrity/security blockers; CONDITIONAL only for explicitly optional limitations; FAILED for any mandatory unverified gate. Ledger starts unimplemented. Include portfolio narrative that distinguishes personal capstone from employed production operations; cite measured lab results with profile.
''')

for name,body in {
 'pull_request.md':'Requirement IDs / problem:\n\nResulting behavior and concrete before/after:\n\nContract/schema impact and old consumers:\n\nValidation evidence (positive,negative,race,failure):\n\nDeploy/rollback + migration compatibility:\n\nSecurity/telemetry impact and limitations:',
 'issue-story.md':'Story ID / actor / goal:\n\nContext and preconditions:\n\nMain / alternative / error cases:\n\nGiven / When / Then:\n\nDependencies / owned service / screen:\n\nEvidence and reviewer:',
 'issue-bug.md':'Expected / actual:\n\nLab profile/commit/digests/fixture/time:\n\nMinimal reproduction:\n\nCorrelation/state/trace (redacted):\n\nImpact and suspected boundary:\n\nRegression acceptance:',
 'incident-report.md':'Incident ID / UTC timeline / owner / severity:\n\nCustomer and invariant impact:\n\nDetection (metric/trace):\n\nTrigger and facts vs hypotheses:\n\nMitigation and recovery evidence:\n\nRoot cause and contributing factors:\n\nFollow-up requirement IDs / owners:\n\nUnresolved delta/limitation:',
 'review-record.md':'Milestone/requirements:\n\nReviewer/date/environment:\n\nEvidence paths:\n\nCommands actually executed:\n\nQuestions and student explanations:\n\nVerdict pass/failed/blocked:\n\nOpen findings/required rerun:',
 'adr-template.md':'Status / date / requirement IDs:\n\nContext and forces:\n\nDecision:\n\nAlternatives rejected with reason:\n\nConsequences and failure behavior:\n\nExperiment/evidence:\n\nReconsideration trigger:',
 'contract-review.md':'Owner / operation or event / consumers:\n\nOld/new schemas and examples:\n\nSemantic and auth changes:\n\nBackward/forward compatibility risks:\n\nMigration / dual-version duration / DLQ replay:\n\nProvider+consumer evidence:\n\nReviewer verdict:'
}.items(): write('operations/templates/'+name,'# '+name.replace('.md','').replace('-',' ').title()+'\n\n'+body)
write('operations/requirements-evolution.md', '''# Change requests for architecture practice

CR01 partial return: future extension requires per-asset return and settlement partitions, capture schedules, per-item refund bounds; old all-assets event remains supported. Deliver ADR, v2 event, migration/backfill and old consumer tests before feature code.

CR02 another currency: EUR CHECK changes are not enough; quote rate currency, rounding, settlement/refund and provider intent alignment need immutable money value; avoid converting existing bookings in-place. Provide currency invariant and contract impact review.

CR03 move asset depot: Inventory transfer allocation and physical job responsibility; ensure reservations don't follow stale depot projections. Competing reserve/transfer race test and authority fence required.

CR04 PSP outage longer than10min: hold expiry means compensation even if payment result unknown; product may introduce longer holds with explicit capacity cost, not silent timeout increase. Model cash exposure and user pending UI.

CR05 organization grows100depots: query plans, tenants, partitioned routing and metrics cardinality before splitting Inventory; justify bottleneck by measured trace/workload. No invented growth graph.

Each extension includes new story ID, impacted contracts/ER/screens, old-version migration, failure experiment, independent rollout and reviewer questions. Optional work after M18 core gates.
''')

def finish_registry():
    dump('atlas/content.json',dict(services=SERVICES,stories=stories,nfr=[dict(id=i,title=t,acceptance=a,milestone=m) for i,t,a,m in NFR],milestones=milestones,tracks=tracks,technologies=[dict(track=a,name=b,problem=c,alternatives=d,limits=e,learn=f,deliver=g,prove=h) for a,b,c,d,e,f,g,h in TECHS],sources=[dict(id=i,title=t,url=u,status=s) for i,t,g,u,s,n in SOURCES],docs=DOCS))
    write('atlas/content.js','window.DEPOTFLOW = '+json.dumps(json.loads((ROOT/'atlas/content.json').read_text(encoding='utf-8')),ensure_ascii=False)+';')

if __name__=='__main__': finish_registry(); print(f'Generated {len(DOCS)} documents')
