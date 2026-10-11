# Fulfillment logical data model

All id/org/subject references UUID unless OIDC subject opaque string; version BIGINT starts1; time TIMESTAMPTZ UTC. Business text length caps name120, reason1000, serial80. FK only within this database; org_id on every tenant-owned row. DB constraints supplement HTTP validation. Money integer BIGINT; JSON payload schema validated before persistence; no decimal floating point.

## jobs

Columns: id, org_id, booking_id, customer_id, depot_id, asset_ids, start_at, end_at, status, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## handover_records

Columns: id, org_id, job_id, asset_ids, actor_id, occurred_at. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## return_reports

Columns: id, org_id, job_id, condition, late_days, damage_minor, notes, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## booking_projection

Columns: booking_id, org_id, status, last_version, updated_at. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## Constraints / indexes / lifecycle

UNIQUE(org_id,booking_id) job; UNIQUE(job_id) handover and return. booking_projection version monotonic; ownership queries index(org_id,depot_id,status). Return report amount nonnegative, condition enum, timestamps server-generated; serial list snapshot, opaque asset IDs.

Inbox/outbox/idempotency schema described in passport. Relational ER depicts cardinalities, not cross-service joins. Add created_at/updated_at where necessary in migrations; every mutable aggregate update checks version. Write migration forward, clean-install and upgrade-from-previous tests. No production seed fixture in migration. Query plan evidence: EXPLAIN ANALYZE on representative100k rows, record rows/read buffers and selected index; do not disable seqscan to force a desired result.
