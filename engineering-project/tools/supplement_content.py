from build_content import write,DOCS

write('assignments/labs/L01-kafka.md', '''# L01 — Kafka vs RabbitMQ: replayable depot utilization projection

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
''')
write('assignments/labs/L02-grpc.md', '''# L02 — REST vs gRPC availability transport

Context: optional comparative lab after M04, depth recommended during M14. Learn generated contract, HTTP/2, protobuf field compatibility, deadlines and status mapping. Core remains REST unless a measured ADR changes it.

Define protobuf query(model_id,depot_id,start_at,end_at,qty) and response(quantity_available,authoritative_at,guaranteed=false); no business logic solution supplied. Wrapper calls the same Inventory application handler, not a second allocation authority. Implement REST and gRPC clients on identical fixture, TLS locally with trusted lab certificate, propagated deadline. 1000serial and100concurrent read calls, record p50/p95/resources/payload with same network. Compare serialization+transport cost separately from SQL; do not claim gRPC fixes DB latency.

Evolution: add optional field and run old client; reserve deleted field numbers/names and demonstrate why number reuse changes meaning. Invalid interval maps semantic error, timeout DEADLINE_EXCEEDED, permission PERMISSION_DENIED, missing foreign object NOT_FOUND. Block tenant spoofing and expose no private DB. Retry only idempotent query within overall budget; cancellation stops pending client work, not necessarily already completed DB transaction.

Deliverables: .proto, generated code build reproducibility, two client fixtures, TLS/deadline/negative tests, measurement raw data, ADR keep/change. Acceptance: REST/gRPC return identical results for100fixture queries incl invalid/foreign cases; old client reads additive field update; strict deadline test cancels and frees worker; no schema-number reuse. Review: explain protobuf encoding vs domain invariants and why repeated read differs from reserve command. Done after all tests and explicit limitations. No requirement to ship this in main platform.
''')
write('assignments/labs/L03-jenkins.md', '''# L03 — Delivery pipeline comparison: GitHub Actions vs Jenkins

Optional full comparative lab after M13. Core pipeline uses GitHub Actions and portable local check scripts. Objective: separate orchestration tool from actual checks, understand runner trust and delivery secrets.

Use isolated local Jenkins controller/agent image with pinned digest and sandbox repository copy; do not expose Docker socket or personal credentials. Execute the same portable scripts for quote tests, Inventory contention, contract backward compatibility, image build/SBOM and smoke. Controller credentials minimal; no remote push/deploy except isolated namespace. Build one changed service plus reverse contract dependencies, not every service blindly. Publish digest and raw logs as artifacts, no echo-only gates.

Scenarios: failed unit/assertion must stop image promotion; old-consumer failure blocks release; changed shared contract triggers consumers even when service source unchanged; agent restart loses ephemeral workspace but artifact/source manifest permits rerun; missing secret fails safely without logged value. Timeout10min lab job and artifact retention7days design assumptions, measured resource cost compared to GitHub Actions runner/local fallback. Explain hosted runner versus self-hosted trust, webhook/signature, plugin update burden and reproducibility.

Deliverables Jenkinsfile, agent version/digest, permissions diagram, artifact manifest, five negative/failure reports, comparison ADR. Acceptance: same source seed produces identical test verdicts in both orchestrators, untrusted PR cannot access deployment secret, failure exit code not swallowed by shell, no personal profile/settings changed. Review chooses a failed contract and asks where promotion is prevented. Done after actual execution and source review; launching Jenkins UI alone insufficient.
''')
write('operations/tutor-checkpoints.md', '''# Tutor checkpoints and skill evidence

For each milestone: explain concept with one problem from DepotFlow; student predicts positive and failure outcomes; student practices in own isolated lab; inspect raw output and owner states; explain errors using invariant/contract, ask student to propose correction; repeat only failed/changed checks; confirm skill with a new input/race/fault not copied from explanation.

Checkpoint evidence fields: concept, own explanation, prediction, code/command location, observed evidence link, mismatch and correction, independent transfer test, reviewer verdict. Never award skill because technology starts in Compose. Business implementation not pre-written here. If user explicitly asks for a solution later, tutor may provide scoped help; otherwise show reasoning and small practice prompts before code.

Milestone entry questions: M01 socket vs configuration; M02 subject vs organization/role; M03 immutable price; M04 overlap and lock; M05 response-loss vs effect; M06 ACK/confirm boundaries; M07 unknown PSP; M08 compensation race; M09 irreversible physical act; M10 pending refund bound; M11 UI cache vs authority; M12 causal trace; M13 old consumer compatibility; M14 measured percentile/error denominator; M15 readiness/HA; M16 image vs schema rollback; M17 RPO/RTO and reconciliation; M18 explain design trade-offs from actual evidence.
''')
