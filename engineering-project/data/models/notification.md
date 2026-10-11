# Notification logical data model

All id/org/subject references UUID unless OIDC subject opaque string; version BIGINT starts1; time TIMESTAMPTZ UTC. Business text length caps name120, reason1000, serial80. FK only within this database; org_id on every tenant-owned row. DB constraints supplement HTTP validation. Money integer BIGINT; JSON payload schema validated before persistence; no decimal floating point.

## preferences

Columns: id, org_id, subject_id, email_enabled, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## notifications

Columns: id, org_id, subject_id, source_event_id, title, read_at. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## deliveries

Columns: id, org_id, notification_id, channel, status, attempt, next_attempt_at. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## Constraints / indexes / lifecycle

UNIQUE(org_id,subject_id,source_event_id) notifications; INDEX(subject_id,created_at,id) for SSE cursor; delivery UNIQUE(notification_id,channel), index(status,next_attempt_at); read_at TIMESTAMPTZ nullable. Never store full upstream booking payload if only title needed.

Inbox/outbox/idempotency schema described in passport. Relational ER depicts cardinalities, not cross-service joins. Add created_at/updated_at where necessary in migrations; every mutable aggregate update checks version. Write migration forward, clean-install and upgrade-from-previous tests. No production seed fixture in migration. Query plan evidence: EXPLAIN ANALYZE on representative100k rows, record rows/read buffers and selected index; do not disable seqscan to force a desired result.
