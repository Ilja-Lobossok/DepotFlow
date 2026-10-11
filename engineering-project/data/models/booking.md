# Booking logical data model

All id/org/subject references UUID unless OIDC subject opaque string; version BIGINT starts1; time TIMESTAMPTZ UTC. Business text length caps name120, reason1000, serial80. FK only within this database; org_id on every tenant-owned row. DB constraints supplement HTTP validation. Money integer BIGINT; JSON payload schema validated before persistence; no decimal floating point.

## bookings

Columns: id, org_id, customer_id, quote_id, quote_snapshot, status, version, created_at. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## sagas

Columns: id, org_id, booking_id, phase, deadline_at, cancel_requested, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## timeline_entries

Columns: id, org_id, booking_id, source_event_id, type, at. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## Constraints / indexes / lifecycle

UNIQUE(org_id,quote_id,customer_id,operation_id) where operation identifier supplied; repeat same quote with new key may make distinct booking. versions BIGINT optimistic; INDEX(status,deadline_at) on sagas; UNIQUE(source_event_id) timeline within consumer. Quote snapshot immutable JSON validated contract. Cancel tombstone belongs saga/booking, survives terminal state.

Inbox/outbox/idempotency schema described in passport. Relational ER depicts cardinalities, not cross-service joins. Add created_at/updated_at where necessary in migrations; every mutable aggregate update checks version. Write migration forward, clean-install and upgrade-from-previous tests. No production seed fixture in migration. Query plan evidence: EXPLAIN ANALYZE on representative100k rows, record rows/read buffers and selected index; do not disable seqscan to force a desired result.
