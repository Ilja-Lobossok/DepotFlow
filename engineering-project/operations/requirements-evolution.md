# Change requests for architecture practice

CR01 partial return: future extension requires per-asset return and settlement partitions, capture schedules, per-item refund bounds; old all-assets event remains supported. Deliver ADR, v2 event, migration/backfill and old consumer tests before feature code.

CR02 another currency: EUR CHECK changes are not enough; quote rate currency, rounding, settlement/refund and provider intent alignment need immutable money value; avoid converting existing bookings in-place. Provide currency invariant and contract impact review.

CR03 move asset depot: Inventory transfer allocation and physical job responsibility; ensure reservations don't follow stale depot projections. Competing reserve/transfer race test and authority fence required.

CR04 PSP outage longer than10min: hold expiry means compensation even if payment result unknown; product may introduce longer holds with explicit capacity cost, not silent timeout increase. Model cash exposure and user pending UI.

CR05 organization grows100depots: query plans, tenants, partitioned routing and metrics cardinality before splitting Inventory; justify bottleneck by measured trace/workload. No invented growth graph.

Each extension includes new story ID, impacted contracts/ER/screens, old-version migration, failure experiment, independent rollout and reviewer questions. Optional work after M18 core gates.
