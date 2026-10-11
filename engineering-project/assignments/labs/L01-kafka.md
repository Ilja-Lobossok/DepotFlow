# L01 — Kafka vs RabbitMQ: replayable depot utilization projection

## Context / Learning objectives
Mandatory comparison during M14, not a replacement for core RabbitMQ. Understand why a log and a work queue have different replay/ordering/operational costs. Prerequisites M06/M08; outbox/inbox and aggregate versions understood.

## Assignment
In isolated Compose profile add one Kafka broker for learning (not HA claim). Topic depot-utilization.v1 with3partitions, key=booking_id. Publish identical contract-approved booking.confirmed and fulfillment.returned facts from isolated archive replay adapter, not dual-publish business transactions to two brokers as production design. Consumer group utilization-v1 writes own projection DB with event_id dedupe and per-booking state. Calculate scheduled asset-hours by depot/day and outstanding returned/not-returned bookings, based on quote UTC period and qty. Returned arriving first parks until booking context known; no negative utilization. Projection is read-only and has no money/availability authority.

## Technical / functional requirements
Archive1000bookings with10% repeated event deliveries and randomized order across keys, publish stable IDs; per-key ordering only. Persist projection+dedupe before committing offset. Crash between DB commit and offset commit must redeliver without double-count. Rebalance group with2→3consumers and inspect partition assignment/lag. Start utilization-v2 new group earliest offsets and rebuild identical result within retained history; retention deletion must explicitly demonstrate inability to reconstruct older data without archive/snapshot.

Run equivalent RabbitMQ consumer on same archived input with same DB invariants. Rabbit queue delivery after ACK cannot itself provide full historical replay; replay requires archive publisher. Compare operating complexity, restart behavior, replay time, ordering, payload/throughput and resource usage under the same hardware. No universal throughput winner claimed from one laptop.

## Deliverables / acceptance
Topic config, consumer/projection schema, archive seed/hash, event contracts, raw offsets/lag/resource reports, replay comparison ADR. Expected output generated independently from archive offline reduction; final totals exact equality for both. Consumer crash before/after commit and rebalance change no result. Different keys may reorder; prove no global-order assumption. Bad payload goes quarantine with source topic/partition/offset, no infinite poison loop. Retention gap recognized, not zero count silently.

## Review / Done / advanced
Reviewer picks offset crash boundary and asks why committing offset first loses data. Explain broker exactly-once claim vs external SQL side effect. Done when comparisons reproducible and limitations recorded; no core saga migrated to Kafka without new ADR. Advanced: transactional producer, compacted snapshot topic, partition count evolution with migration review.
