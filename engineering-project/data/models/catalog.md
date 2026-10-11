# Catalog logical data model

All id/org/subject references UUID unless OIDC subject opaque string; version BIGINT starts1; time TIMESTAMPTZ UTC. Business text length caps name120, reason1000, serial80. FK only within this database; org_id on every tenant-owned row. DB constraints supplement HTTP validation. Money integer BIGINT; JSON payload schema validated before persistence; no decimal floating point.

## models

Columns: id, org_id, name, category, active, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## rates

Columns: id, org_id, model_id, daily_minor, deposit_minor, currency, valid_from, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## quotes

Columns: id, org_id, model_id, depot_id, start_at, end_at, quantity, days, daily_minor, rental_minor, deposit_minor, currency, expires_at, rate_version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## Constraints / indexes / lifecycle

Rates immutable; INDEX(org_id,model_id,valid_from DESC). Quote stores all money amounts as BIGINT≥0, currency CHECK EUR, timestamps TIMESTAMPTZ, days INTEGER≥1. Quote retains rate_version; model delete forbidden once quoted, soft deactivate.

Inbox/outbox/idempotency schema described in passport. Relational ER depicts cardinalities, not cross-service joins. Add created_at/updated_at where necessary in migrations; every mutable aggregate update checks version. Write migration forward, clean-install and upgrade-from-previous tests. No production seed fixture in migration. Query plan evidence: EXPLAIN ANALYZE on representative100k rows, record rows/read buffers and selected index; do not disable seqscan to force a desired result.
