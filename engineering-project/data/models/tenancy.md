# Tenancy logical data model

All id/org/subject references UUID unless OIDC subject opaque string; version BIGINT starts1; time TIMESTAMPTZ UTC. Business text length caps name120, reason1000, serial80. FK only within this database; org_id on every tenant-owned row. DB constraints supplement HTTP validation. Money integer BIGINT; JSON payload schema validated before persistence; no decimal floating point.

## organizations

Columns: id, name, status, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## memberships

Columns: id, org_id, subject_id, role, depot_id?, status, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## audit_entries

Columns: id, org_id, actor_id, action, target_id, occurred_at. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## Constraints / indexes / lifecycle

UNIQUE(org_id,subject_id); membership role CHECK listed role; depot nullable except operator. Index active memberships by(org,subject), audit(org,occurred_at). Tenancy does not FK to Inventory depot; validate authoritative depot GET on assignment.

Inbox/outbox/idempotency schema described in passport. Relational ER depicts cardinalities, not cross-service joins. Add created_at/updated_at where necessary in migrations; every mutable aggregate update checks version. Write migration forward, clean-install and upgrade-from-previous tests. No production seed fixture in migration. Query plan evidence: EXPLAIN ANALYZE on representative100k rows, record rows/read buffers and selected index; do not disable seqscan to force a desired result.
