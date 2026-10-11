# Tenancy — service passport

## Responsibility / boundary
Организации, членство, роли и допуск к складам. Не хранит пароли; Keycloak аутентифицирует, Tenancy решает бизнес-доступ.

## Stack
Java21, Spring Boot4.1 family, Maven wrapper, Spring Security, JDBC explicit transactions, Flyway; pin patch and image digests at M01.
JDBC selected over automatic ORM cascades for visible locking and aggregate transitions; ORM alternative allowed after ADR preserving SQL invariants.

## Data ownership / schema
Database: tenancy_db. Role: tenancy_app. No credentials for other owners.

| Table | Logical columns |
|---|---|
|organizations|id, name, status, version|
|memberships|id, org_id, subject_id, role, depot_id?, status, version|
|audit_entries|id, org_id, actor_id, action, target_id, occurred_at|

Logical model, types/indexes/constraints in data/models/tenancy.md and ER source. Migration implementation remains student work.

## HTTP contract
[OpenAPI](../../contracts/openapi/tenancy.json); public and internal operations clearly tagged. The API is a design specification, not a running server.

## Events / dependencies
Publishes: membership.changed. Consumes: none.
[Per-service AsyncAPI](../../contracts/asyncapi/tenancy.json). Dependencies follow named commands/GETs; all services depend on Tenancy for mutation authorization, Keycloak JWKS, own DB and telemetry. Catalog/Notification use Redis/SSE as specified; Billing alone calls PSP; Fulfillment claims Booking; Booking fetches immutable Catalog quote snapshot and owner recovery status.

## Failure behavior
Недоступность Tenancy блокирует новые бизнес-команды (503), чтения возможны с membership snapshot не старше 60 s.

## Metrics and scaling
authorization_denied_total; membership_check_seconds. Stateless HTTP replicas; membership lookup indexes; no shared auth cache without bounded revocation.

## Service-specific checks
Два tenant, отозванная роль, чужой depot, audit without token data.

## Configuration / identity
Env names: SERVICE_PORT, DB_URL, DB_USER, DB_PASSWORD_FILE, AMQP_URL, OIDC_ISSUER, OIDC_AUDIENCE, OTEL_EXPORTER_OTLP_ENDPOINT, LOG_LEVEL. Private credentials via mounted secret, no committed .env with secrets. Validate required config at startup; store exact versions/digests in implementation lock file at M01. HTTP resource server JWT issuer/audience/expiry; internal credentials scoped per caller; tenant/subject contextual authorization survives gateway. Membership authoritative check on business writes. Broker ACL read/write only named queues/exchanges.

## Errors / health / deployment
RFC-style problem response: type, title, status, code, correlationId, violations (safe paths only); stable codes in contracts. 401 invalid auth;403 forbidden own resource;404 missing/foreign;409 business conflict;412 stale version;422 semantic validation;428 missing precondition;429 throttled;503 unavailable dependency. Liveness checks process only; startup validates migrations/config; readiness DB reachable, essential HTTP workers ready; broker outage marks async degradation and metrics, does not restart all services. Non-root container, readonly root filesystem, writable temp only, graceful drain30s; separate migration job; requests/limits measured in M15. Own image deployable without rebuilding peers.

## Private persistence / messaging
Each owner additionally has outbox(event_id UNIQUE, aggregate_id, payload, status, created_at), inbox(consumer,event_id UNIQUE, received_at), idempotency(org,subject,route,key UNIQUE, request_hash, response, expires_at). A service without outbound messages need not create outbox. Producer aggregate_version monotonic per aggregate; command_id stable across redelivery; consumer dedupe persists with business changes. No foreign-service DB permissions. Foreign IDs are opaque and validated via contract, no cross-DB FK.

## Test suite
Unit: pure transition rules, validation and money boundaries. Integration: PostgreSQL real transactions and migrations via Testcontainers; RabbitMQ ack/confirm tests where used. Contract: generated schema fixtures and provider/consumer compatibility. E2E: only exposed APIs and owned-state diagnostic reports, never foreign DB writes. Include tenant isolation, dependency timeout, duplicate and restart tests. Expose metrics without customer/booking high-cardinality labels; JSON logs with trace_id and correlation_id but no JWT or PII. See reviews/test-strategy.md.
