# Business logic — authoritative process specification

Все часы сохраняются в UTC; deadline проверяет время БД, не браузера. IDs UUID; внешние ссылки принадлежат org. Чтение чужого объекта даёт404; запрещённая операция над своим —403. Проверка membership Tenancy синхронная на каждой изменяющей business command; кеш чтений≤60s. State transition и outbox пишутся одной транзакцией владельца. Inbox уникален (consumer,event_id); ack только после commit. Ниже правила обязательны совместно, не альтернативные варианты.

## P01 — Quote

**Actors / authorization:** customer; Catalog.

**Initial conditions:** active model/rate; trusted org membership.

**Actions / validation:** Validate UTC interval, qty; read rate in one transaction, snapshot price and expires_at. Return201 quote ID.

**States / concurrency / forbidden transitions:** ACTIVE→EXPIRED by time; immutable body. Expired reuse422. Concurrent rate update cannot mix deposit/rental versions.

**Retries / cancellation / partial failure / expected outcome:** Retry create same key returns same quote. Cancel has no side effect; no money reserved. Catalog/DB fail503; UI re-quotes only after user consent.

## P02 — Reserve

**Actors / authorization:** Booking → Inventory.

**Initial conditions:** persisted pending booking; valid quote snapshot.

**Actions / validation:** Publish reserve-requested via outbox; Inventory selects qty assets in ID order, locks asset rows, checks maintenance and allocation overlap, commits all-or-nothing hold+allocation+outbox.

**States / concurrency / forbidden transitions:** REQUESTED→HELD or REJECTED; HELD→COMMITTED/EXPIRED/RELEASED. Tenant+asset+overlap exclusion, maintenance same allocation table. Failure to acquire any unit rolls back all.

**Retries / cancellation / partial failure / expected outcome:** Command identity booking_id. Multiple identical commands return same outcome event with stable ID/outbox identity; different parameters409. Expire sweep locks hold, sets allocation inactive; time guard on commit wins over delayed sweep.

## P03 — Authorize & commit

**Actors / authorization:** Booking → Billing → Inventory.

**Initial conditions:** Held; no cancel requested; deadline=min(holdExpiry, sagaDeadline).

**Actions / validation:** Billing authorizes rental+deposit using provider_key=booking+authorize:v1. Save authorized result/outbox. Booking publishes commit; Inventory under hold lock checks DB time<expires_at and alloc active; emits committed.

**States / concurrency / forbidden transitions:** Booking PENDING→CONFIRMED only after allocation.committed AND authorized intent correlation. Expiry or rejection→COMPENSATING→CANCELLED/FAILED after release+void evidence.

**Retries / cancellation / partial failure / expected outcome:** PSP call may succeed while response lost: UNKNOWN, reconcile query by key; never generate new provider key. Late authorized after compensation -> void. Late committed while cancel intent -> release. Terminal state suppresses stale forward transitions.

## P04 — Cancel

**Actors / authorization:** customer; Booking saga.

**Initial conditions:** own booking pending/confirmed; no handover claim.

**Actions / validation:** Atomic booking lock records cancel_requested and version; emit release+void commands if corresponding steps exist. Confirm completion only with observed allocation released and intent voided/no intent.

**States / concurrency / forbidden transitions:** PENDING/CONFIRMED→CANCELLING→CANCELLED; concurrent handover claim→409. No cancellation after irreversible handover.

**Retries / cancellation / partial failure / expected outcome:** Repeated same cancellation returns same intent. Partial dependency failure leaves CANCELLING and reconciliation age visible; deadline does not imply compensation success. Cancel-before-hold sets tombstone to reject later hold/commit.

## P05 — Handover fence

**Actors / authorization:** operator; Fulfillment + Booking.

**Initial conditions:** same depot, confirmed, active allocation, within pickup window.

**Actions / validation:** Fulfillment calls Booking claim with job_id and expected version. Booking atomic CONFIRMED→HANDOVER_CLAIMED; cancel now forbidden. Fulfillment persists physical act and event; Booking becomes IN_USE after event.

**States / concurrency / forbidden transitions:** CONFIRMED→HANDOVER_CLAIMED→IN_USE. Claim idempotent per job; another job409. Claim without completed act after timeout→MANUAL_REVIEW, no automatic release.

**Retries / cancellation / partial failure / expected outcome:** Before physical transfer verify exact serial IDs locally against immutable confirmed allocation snapshot. Lost claim response re-query; never hand over on timeout. Operator must explicitly resolve claim incident; no TTL unlock of possible physical transfer.

## P06 — Return & quarantine

**Actors / authorization:** operator; Fulfillment → Inventory.

**Initial conditions:** handover act present; same depot; all assets.

**Actions / validation:** One transaction return report+jobReturned+outbox. Inventory marks original allocation inactive, good asset READY, damaged asset QUARANTINED with maintenance block. Emits allocation.released.

**States / concurrency / forbidden transitions:** Job IN_USE→RETURNED; Booking IN_USE→SETTLING. Asset READY→RENTED→READY/QUARANTINED. Out-of-order return before handed-over event requires entity lookup/parking.

**Retries / cancellation / partial failure / expected outcome:** Unique report per job; duplicate same command same report, different body409. If future allocation overlaps new quarantine, do not erase it: mark asset unavailable, incident and notify Booking to stop handover. Settlement blocked until release acknowledged.

## P07 — Settle

**Actors / authorization:** Booking → Billing.

**Initial conditions:** return report and allocation release; authorized intent.

**Actions / validation:** Calculate immutable settlement from quote and return. Capture cost≤authorized; void unused authorization. Persist operation IDs/ledger; reconcile unknown PSP separately.

**States / concurrency / forbidden transitions:** AUTHORIZED→CAPTURE_PENDING→CAPTURED or UNKNOWN; excess→MANUAL_REVIEW. Booking SETTLING→COMPLETED only after captured + remainder void or full void for zero cost.

**Retries / cancellation / partial failure / expected outcome:** Duplicate settlement operation returns prior amount; changed amount409. Capture+void must reconcile independently. Failure does not reallocate returned equipment. Customer sees settlement pending; no phantom complete.

## P08 — Refund

**Actors / authorization:** finance; Billing.

**Initial conditions:** captured remainder>0; reason and If-Match.

**Actions / validation:** Lock intent, reserve refundable amount for pending operation, persist request; invoke PSP stable key outside lock; finalize ledger from response/webhook.

**States / concurrency / forbidden transitions:** CAPTURED→REFUND_PENDING→PARTIALLY_REFUNDED/REFUNDED; UNKNOWN waits reconciliation. captured-refunded-pending_refunds≥0 invariant.

**Retries / cancellation / partial failure / expected outcome:** Concurrent full refunds cannot each reserve same remainder. Cancel refund before provider call optional; after call do not assume cancellation. Duplicate signed webhook unique provider_event_id; conflicting payload quarantined.

## P09 — Repair

**Actors / authorization:** operator; Inventory.

**Initial conditions:** asset not rented; no conflicting committed interval.

**Actions / validation:** Under asset lock create maintenance allocation, asset QUARANTINED; repair records reason and completed inspection; deactivate maintenance block and mark READY.

**States / concurrency / forbidden transitions:** READY→QUARANTINED→READY; cannot jump RENTED→READY without return. Future reservation conflicts return409 with dispatcher action.

**Retries / cancellation / partial failure / expected outcome:** Concurrent maintenance/hold share asset lock and exclusion invariant. Retry same key same maintenance job; changed reason conflicts. Operator access depot-scoped.

## P10 — Notification

**Actors / authorization:** Notification.

**Initial conditions:** recognized event; valid tenant and subject.

**Actions / validation:** Inbox dedupe + notification + delivery plan atomic; sender retries mail sink with stable Message-ID; UI SSE sends IDs and cursor.

**States / concurrency / forbidden transitions:** delivery PENDING→SENT or RETRY→DLQ; read_at independent. Projection versions only advance.

**Retries / cancellation / partial failure / expected outcome:** Duplicates do not produce duplicate UI rows, but external email can duplicate after ambiguous delivery. Retry 5 attempts; inbox replay policy required when retention reached. Disconnect uses HTTP snapshot, no correctness dependency on SSE.

## Booking state machine

PENDING → CONFIRMED | COMPENSATING | CANCELLING; CONFIRMED → HANDOVER_CLAIMED | CANCELLING; HANDOVER_CLAIMED → IN_USE | MANUAL_REVIEW; IN_USE → SETTLING; SETTLING → COMPLETED | MANUAL_REVIEW; CANCELLING/COMPENSATING → CANCELLED/FAILED only after compensation evidence. FAILED/CANCELLED/COMPLETED terminal for forward business changes; late events can still cause compensating commands and audit rows. Refund never changes COMPLETED booking back to SETTLING. Manual review resolutions require reason, role and bounded state transition; no arbitrary status field setter API.

## Event ordering rule

Events carry producer aggregate_version and event_id; facts may arrive late. Consumers dedupe by ID and check event-specific prerequisites. Full snapshot projections ignore lower version; business facts are not discarded solely for low version (a late authorization still needs void). Gap -> park event with reason and perform authoritative GET; retry then DLQ if schema invalid. Commands have command_id plus expected correlation, idempotent by business operation; cancellation tombstone prevents resurrection. No total order across services.

## Physical overrun

Rental interval conflict guarantees promises based on scheduled return, not physically timely return. Sweep after end+15min for IN_USE assets marks unavailable and emits asset.unavailable; future job handover must reject absent asset. Inventory raises incident listing affected bookings. Dispatcher may cancel before claim or perform advanced replacement saga. Do not automatically refund/replace a physical asset silently. Test overrun against future committed allocation explicitly.

## Physical eligibility before claim

Fulfillment GET Inventory /internal/v1/bookings/{booking_id}/handover-check immediately before Booking claim. If not eligible/unavailable, stop; if check succeeds then claim serializes cancellation. Same job serialized at Fulfillment. Inventory consumes handed-over to mark RENTED; late return/handover uses job history not message arrival order. Operator verifies physical serial/condition before actual transfer; this physical check is required even if projection says READY. A failure after claim leaves manual review, not timed auto release.

## Membership safety

Tenancy rejects revocation/demotion of last active org_admin with409 last_admin; locks organization and memberships atomically to prevent concurrent removal of two last admins. Invite/role update cannot assign operator without a valid same-org depot. Audit actor/reason/version persists with membership change. Initial org and first admin are synthetic bootstrap fixtures, not open public sign-up in core.
