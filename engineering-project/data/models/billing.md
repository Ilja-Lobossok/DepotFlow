# Billing logical data model

All id/org/subject references UUID unless OIDC subject opaque string; version BIGINT starts1; time TIMESTAMPTZ UTC. Business text length caps name120, reason1000, serial80. FK only within this database; org_id on every tenant-owned row. DB constraints supplement HTTP validation. Money integer BIGINT; JSON payload schema validated before persistence; no decimal floating point.

## payment_intents

Columns: id, org_id, booking_id, customer_id, authorized_minor, captured_minor, refunded_minor, pending_refund_minor, status, provider_key, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## payment_operations

Columns: id, org_id, intent_id, kind, amount_minor, provider_key, status, attempt, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## provider_events

Columns: id, provider_event_id, intent_id, signature_valid, received_at. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## ledger_entries

Columns: id, org_id, intent_id, operation_id, kind, amount_minor, created_at. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## Constraints / indexes / lifecycle

BIGINT money, nonnegative; captured<=authorized; refunded+reserved_pending_refunds<=captured. UNIQUE(org_id,booking_id) intent; UNIQUE(operation_id) ledger; UNIQUE provider_event_id. No ledger row mutation/delete; reversal new entry. PSP pending operation table required to persist amount reservation and outcome independently of network call.

Inbox/outbox/idempotency schema described in passport. Relational ER depicts cardinalities, not cross-service joins. Add created_at/updated_at where necessary in migrations; every mutable aggregate update checks version. Write migration forward, clean-install and upgrade-from-previous tests. No production seed fixture in migration. Query plan evidence: EXPLAIN ANALYZE on representative100k rows, record rows/read buffers and selected index; do not disable seqscan to force a desired result.
