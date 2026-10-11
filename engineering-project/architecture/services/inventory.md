# Inventory — service passport

## Responsibility / boundary
Экземпляры, временные allocations, holds, ремонт и доступность. Единственный авторитет по пересечению интервалов; Availability UI — подсказка.

## Stack
Java21, Spring Boot4.1 family, Maven wrapper, Spring Security, JDBC explicit transactions, Flyway; pin patch and image digests at M01.
JDBC selected over automatic ORM cascades for visible locking and aggregate transitions; ORM alternative allowed after ADR preserving SQL invariants.

## Data ownership / schema
Database: inventory_db. Role: inventory_app. No credentials for other owners.

| Table | Logical columns |
|---|---|
|depots|id, org_id, name, timezone|
|assets|id, org_id, model_id, depot_id, serial, state, version|
|holds|id, org_id, booking_id, expires_at, status, version|
|allocations|id, org_id, asset_id, hold_id?, booking_id?, kind, period, active, version|
|maintenance_jobs|id, org_id, asset_id, reason, status, version|
|release_tombstones|id, org_id, booking_id, reason, created_at|

Logical model, types/indexes/constraints in data/models/inventory.md and ER source. Migration implementation remains student work.

## HTTP contract
[OpenAPI](../../contracts/openapi/inventory.json); public and internal operations clearly tagged. The API is a design specification, not a running server.

## Events / dependencies
Publishes: hold.created, hold.rejected, hold.expired, allocation.committed, allocation.released, asset.unavailable. Consumes: booking.reserve-requested, booking.commit-requested, booking.release-requested, fulfillment.returned, fulfillment.handed-over.
[Per-service AsyncAPI](../../contracts/asyncapi/inventory.json). Dependencies follow named commands/GETs; all services depend on Tenancy for mutation authorization, Keycloak JWKS, own DB and telemetry. Catalog/Notification use Redis/SSE as specified; Billing alone calls PSP; Fulfillment claims Booking; Booking fetches immutable Catalog quote snapshot and owner recovery status.

## Failure behavior
Если Inventory недоступен, booking остаётся pending; никогда не предполагает успешный резерв по timeout.

## Metrics and scaling
allocation_conflict_total; hold_expired_total; allocation_transaction_seconds. Выбор экземпляров в стабильном порядке; locks и exclusion invariant; replicas не обходят БД.

## Service-specific checks
100 checkout на один asset; hold expiration/commit race; ремонт против резерва.

## Configuration / identity
Env names: SERVICE_PORT, DB_URL, DB_USER, DB_PASSWORD_FILE, AMQP_URL, OIDC_ISSUER, OIDC_AUDIENCE, OTEL_EXPORTER_OTLP_ENDPOINT, LOG_LEVEL. Private credentials via mounted secret, no committed .env with secrets. Validate required config at startup; store exact versions/digests in implementation lock file at M01. HTTP resource server JWT issuer/audience/expiry; internal credentials scoped per caller; tenant/subject contextual authorization survives gateway. Membership authoritative check on business writes. Broker ACL read/write only named queues/exchanges.

## Errors / health / deployment
RFC-style problem response: type, title, status, code, correlationId, violations (safe paths only); stable codes in contracts. 401 invalid auth;403 forbidden own resource;404 missing/foreign;409 business conflict;412 stale version;422 semantic validation;428 missing precondition;429 throttled;503 unavailable dependency. Liveness checks process only; startup validates migrations/config; readiness DB reachable, essential HTTP workers ready; broker outage marks async degradation and metrics, does not restart all services. Non-root container, readonly root filesystem, writable temp only, graceful drain30s; separate migration job; requests/limits measured in M15. Own image deployable without rebuilding peers.

## Private persistence / messaging
Each owner additionally has outbox(event_id UNIQUE, aggregate_id, payload, status, created_at), inbox(consumer,event_id UNIQUE, received_at), idempotency(org,subject,route,key UNIQUE, request_hash, response, expires_at). A service without outbound messages need not create outbox. Producer aggregate_version monotonic per aggregate; command_id stable across redelivery; consumer dedupe persists with business changes. No foreign-service DB permissions. Foreign IDs are opaque and validated via contract, no cross-DB FK.

## Test suite
Unit: pure transition rules, validation and money boundaries. Integration: PostgreSQL real transactions and migrations via Testcontainers; RabbitMQ ack/confirm tests where used. Contract: generated schema fixtures and provider/consumer compatibility. E2E: only exposed APIs and owned-state diagnostic reports, never foreign DB writes. Include tenant isolation, dependency timeout, duplicate and restart tests. Expose metrics without customer/booking high-cardinality labels; JSON logs with trace_id and correlation_id but no JWT or PII. See reviews/test-strategy.md.

## Physical lifecycle

Consumes fulfillment.handed-over to mark RENTED. Return-first events park until handover lookup and then finalize; a late handover fact never changes RETURNED asset back to RENTED. release_tombstones UNIQUE(org_id,booking_id) prevent delayed reserve resurrection. Handover-check validates active committed allocation and current physical readiness before claim; failure blocks physical action.
