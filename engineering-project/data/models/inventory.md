# Inventory logical data model

All id/org/subject references UUID unless OIDC subject opaque string; version BIGINT starts1; time TIMESTAMPTZ UTC. Business text length caps name120, reason1000, serial80. FK only within this database; org_id on every tenant-owned row. DB constraints supplement HTTP validation. Money integer BIGINT; JSON payload schema validated before persistence; no decimal floating point.

## depots

Columns: id, org_id, name, timezone. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## assets

Columns: id, org_id, model_id, depot_id, serial, state, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## holds

Columns: id, org_id, booking_id, expires_at, status, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## allocations

Columns: id, org_id, asset_id, hold_id?, booking_id?, kind, period, active, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## maintenance_jobs

Columns: id, org_id, asset_id, reason, status, version. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## release_tombstones

Columns: id, org_id, booking_id, reason, created_at. Primary key id (projection: booking_id); inherited org scope except global provider event. Required unless '?'; status/role enum defined in business spec. Foreign refs to other service IDs are opaque, not FK.

## Constraints / indexes / lifecycle

allocations.period TSTZRANGE [), bounded, nonempty; CHECK start<end. EXCLUDE GiST(org_id WITH =,asset_id WITH =,period WITH &&) WHERE(active); btree_gist extension prerequisite. All reserve/maintenance/return commands serialize on asset rows. Partial index holds(status,expires_at); UNIQUE org+serial. Expired holds keep active allocation until explicit transition; no volatile now() in index predicate. Repair quarantine can coexist with already committed future allocations only via unavailable asset flag; never insert overlapping maintenance row to bypass invariant.

Inbox/outbox/idempotency schema described in passport. Relational ER depicts cardinalities, not cross-service joins. Add created_at/updated_at where necessary in migrations; every mutable aggregate update checks version. Write migration forward, clean-install and upgrade-from-previous tests. No production seed fixture in migration. Query plan evidence: EXPLAIN ANALYZE on representative100k rows, record rows/read buffers and selected index; do not disable seqscan to force a desired result.
