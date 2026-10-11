# Engineering process / onboarding

Monorepo target: apps/web, services/{tenancy,catalog,inventory,booking,billing,fulfillment,notification}, contracts, platform/{compose,helm,iac,ansible}, docs, tests/{contract,e2e,load,resilience}, evidence. This pack is specification only; student creates implementation repository separately. No Git initialization/commit/push performed here.

Small trunk-based changes on codex/<topic> (or team convention), PR to protected main, no direct main writes. Feature flag incomplete behavior; each PR one explainable risk. Commit reviewed by student, no automatic commit/push by tutor. Independent semantic image tag + immutable digest per service, package source commit recorded.

Coding: strict TS, no any to bypass network validation; Java explicit aggregate boundaries and constructor dependencies; controller validates transport, domain enforces invariants, repository owns SQL; never call PSP under long DB transaction. Formatting automated per language, meaningful tests for invariants. Money utility immutable, no duplicated arithmetic assumptions. Error codes stable; logs JSON, no tokens. Graceful shutdown/health per passport.

Definition of Ready: requirement ID and intent, contract/state impact, fixtures, negative/failure acceptance, known dependencies, reviewable scope. Definition of Done: code + own migration + contract review + positive/negative/failure evidence + docs/diagram updates + clean-start + reviewer approval + known limitation entry. Coverage percentage/checkbox alone not Done.

PR checklist: ownership intact? who can call? race proof? operation key stable? timeout unknown? outbox/inbox transaction boundaries? retry bounded? schema old reader compatibility? resource/log/security impact? deployment/rollback and migration evidence? Student must explain without generated answer memorization.

Backlog epics: E01 Identity/catalog M01–M03; E02 Inventory/booking M04–M05; E03 Delivery/saga M06–M08; E04 Warehouse/finance M09–M10; E05 UI/telemetry M11–M12; E06 Reliability/platform M13–M17; E07 Audit M18. Stories F01–F20 map to milestones; each milestone splits tasks: design contract, implement owner, validate negative/fault, reviewer evidence. Tasks have unique <Mxx>-T01..T04, no generic done flag without tests.

Contract review: proposed change, old/new examples, semantics/authorization, impacted consumers, compatibility fixture gate. Optional fields are additive only if old reader ignores unknown fields; new enum values may break generated exhaustive clients -> deploy tolerant reader first. Breaking event type new major, coexist ≥two releases, do not delete v1 until all consumers upgraded and DLQ/history migration decided. Data migrations expand(add nullable/new table)→dual write/backfill measured idempotently→switch reader→contract later release; backward compatible rollback uses old image with expanded schema. No drop/rename in same release.

Onboarding: read README/PRD, run dependency checks in isolated lab, compare ER/contract to story, implement M01 then follow DAG; explain each shell command before using it. Tutor sequence: explanation → independent practice → inspect evidence → error analysis → skill confirmation. If implementation is requested later, don't supply full solution unless user explicitly asks. Keep evidence raw; failed experiment teaches more than guessed success.
