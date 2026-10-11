# Nonfunctional requirements

Пороги — учебные design targets, не измеренные показатели готового приложения.

## N01: Latency

На lab-standard: 20 virtual users, 10 min after 2min warmup; read p95≤300ms, command acceptance p95≤500ms; saga completion p95≤5s при здоровом PSP; error<1% excluding expected409/422.

Этап: M14. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.

## N02: Integrity

100 concurrent overlapping bookings on one asset produce exactly one committed allocation. Zero overlap, overcapture and duplicate refund across 10k duplicate/reordered deliveries.

Этап: M08. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.

## N03: Tenant isolation

Two organizations × all role/endpoint pairs; no foreign records, events, SSE or cache entries; 401/403/404 verified before access.

Этап: M02. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.

## N04: Recovery

Broker outage120s, consumer killed after DB commit beforeACK; pending saga reconciles ≤120s after recovery for 100 bookings; DLQ poison remains quarantined.

Этап: M14. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.

## N05: Observability

100% synthetic test traces sampled; booking→outbox→consumer→PSP causality queryable; logs correlate; metrics have no booking/customer label.

Этап: M12. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.

## N06: Availability target

Lab SLO 99% successful eligible commands over 1h controlled run (denominator excludes auth/validation/conflict; includes dependency5xx). No claim about monthly production availability.

Этап: M14. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.

## N07: Security

TLS on ingress and internal production-like traffic, JWT issuer/audience/expiry checked, secrets absent repository/logs, least-privilege DB/broker roles; security scenario suite passes.

Этап: M15. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.

## N08: Delivery independence

Seven service images and DB migration streams; notification-only release changes no other digest; each service tests/builds/deploys without importing other business implementation.

Этап: M16. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.

## N09: Accessibility

Keyboard complete customer checkout and operator return; visible focus; labels/errors; no color-only state; contrast normal text≥4.5:1; 360px without horizontal page scroll.

Этап: M11. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.

## N10: Backup

Snapshot RPO target≤24h; measured isolated restore RTO≤30min for fixture dataset; reconnect mismatched service snapshots through reconcile, report unrecoverable delta.

Этап: M17. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.

## N11: Data lifecycle

Synthetic users only; auth logs7d, telemetry7d, notifications30d, inbox/idempotency24h minimum with replay rules; booking/ledger retained for lab history; scrub demo emails on exports.

Этап: M15. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.

## N12: Reproducibility

Clean lab host builds pinned images/contracts; bootstrap docs checked by reviewer; no mandatory external cloud, CDN or paid integration.

Этап: M18. Evidence: raw sample, environment manifest, test ID, timestamps, verdict; failed result не скрывать.
