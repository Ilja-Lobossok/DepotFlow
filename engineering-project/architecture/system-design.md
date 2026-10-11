# System design

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
