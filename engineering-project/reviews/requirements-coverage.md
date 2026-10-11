# Матрица покрытия

Coverage означает наличие спецификации и критериев, а не реализованную бизнес-систему. Все F/N/A реализации UNSTARTED.

| ID | Specification | Assignment | Acceptance | Implementation |
|---|---|---|---|---|
|F01|[product/stories/F01.md](../product/stories/F01.md)|[assignments/M02.md](../assignments/M02.md)|Given A/B; When member A GET booking B; Then 404 и тело без PII. Revocation запрещает команды сразу после authoritative check, чтения ≤60 s.|unstarted|
|F02|[product/stories/F02.md](../product/stories/F02.md)|[assignments/M03.md](../assignments/M03.md)|Given rate 2500; When rate changes to 3000 after quote; Then existing quote uses 2500 until expiry.|unstarted|
|F03|[product/stories/F03.md](../product/stories/F03.md)|[assignments/M04.md](../assignments/M04.md)|When 26 models with page limit 25; Then second cursor returns last item without duplicate. Availability never guarantees allocation.|unstarted|
|F04|[product/stories/F04.md](../product/stories/F04.md)|[assignments/M03.md](../assignments/M03.md)|Given 25 h, qty2, rate2500, deposit10000 per unit; Then days2, rental10000, deposit20000, total authorization30000.|unstarted|
|F05|[product/stories/F05.md](../product/stories/F05.md)|[assignments/M05.md](../assignments/M05.md)|Given one asset; When 100 unique bookings overlap; Then exactly 1 hold, 99 rejections, zero overlapping active allocations.|unstarted|
|F06|[product/stories/F06.md](../product/stories/F06.md)|[assignments/M07.md](../assignments/M07.md)|Given authorization succeeds and allocation commits; Then one confirmed booking, one active allocation, one authorization; 10 duplicate events change none of these counts.|unstarted|
|F07|[product/stories/F07.md](../product/stories/F07.md)|[assignments/M05.md](../assignments/M05.md)|When retry 20 times after response loss; Then one booking and one operation; tenant B may reuse same key independently.|unstarted|
|F08|[product/stories/F08.md](../product/stories/F08.md)|[assignments/M08.md](../assignments/M08.md)|When cancel races allocation commit; Then terminal cancelled eventually has no active allocation and net captured0; timeout alone is not cancelled completion.|unstarted|
|F09|[product/stories/F09.md](../product/stories/F09.md)|[assignments/M09.md](../assignments/M09.md)|When cancel and handover claim race; Then exactly one wins. Double handover returns original act; different payload ->409.|unstarted|
|F10|[product/stories/F10.md](../product/stories/F10.md)|[assignments/M09.md](../assignments/M09.md)|When return event delivered 10 times; Then one report, one release, one settlement; damaged asset not bookable until repair.|unstarted|
|F11|[product/stories/F11.md](../product/stories/F11.md)|[assignments/M10.md](../assignments/M10.md)|Given authorized15000, rental5000, late2500, damage1000; Then capture8500 and void remaining6500, captured-refunded=8500.|unstarted|
|F12|[product/stories/F12.md](../product/stories/F12.md)|[assignments/M10.md](../assignments/M10.md)|When two concurrent full refunds; Then total refunded ≤ captured and one succeeds; second conflicts.|unstarted|
|F13|[product/stories/F13.md](../product/stories/F13.md)|[assignments/M04.md](../assignments/M04.md)|When maintenance period overlaps a committed booking; Then409 and no maintenance insert; after successful repair new hold is permitted.|unstarted|
|F14|[product/stories/F14.md](../product/stories/F14.md)|[assignments/M11.md](../assignments/M11.md)|Given confirmed event duplicated; Then one UI notification; SSE reconnect recovers latest state; email failure leaves confirmed.|unstarted|
|F15|[product/stories/F15.md](../product/stories/F15.md)|[assignments/M12.md](../assignments/M12.md)|When investigate failed booking; Then actor, before/after state, correlation and saga phase are recoverable; timeline rows unique by source event.|unstarted|
|F16|[product/stories/F16.md](../product/stories/F16.md)|[assignments/M04.md](../assignments/M04.md)|When two forms edit same asset at v3; Then first creates v4, second412 and cannot overwrite.|unstarted|
|F17|[product/stories/F17.md](../product/stories/F17.md)|[assignments/M13.md](../assignments/M13.md)|Given old consumer fixture; When optional field added; Then both deserialize; breaking fixture rejected before release.|unstarted|
|F18|[product/stories/F18.md](../product/stories/F18.md)|[assignments/M14.md](../assignments/M14.md)|Given crash after DB commit before ACK; When restarted and replayed; Then one business effect and no lost transition.|unstarted|
|F19|[product/stories/F19.md](../product/stories/F19.md)|[assignments/M16.md](../assignments/M16.md)|When deploy Notification only; Then six core service digests stay unchanged; rollback restores prior image without DB loss.|unstarted|
|F20|[product/stories/F20.md](../product/stories/F20.md)|[assignments/M17.md](../assignments/M17.md)|When restore controlled checkpoint; Then known booking counts, ledger balance and allocation invariants match checkpoint; measured RTO≤30min and snapshot RPO≤24h.|unstarted|
|N01|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M14.md](../assignments/M14.md)|На lab-standard: 20 virtual users, 10 min after 2min warmup; read p95≤300ms, command acceptance p95≤500ms; saga completion p95≤5s при здоровом PSP; error<1% excluding expected409/422.|unstarted|
|N02|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M08.md](../assignments/M08.md)|100 concurrent overlapping bookings on one asset produce exactly one committed allocation. Zero overlap, overcapture and duplicate refund across 10k duplicate/reordered deliveries.|unstarted|
|N03|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M02.md](../assignments/M02.md)|Two organizations × all role/endpoint pairs; no foreign records, events, SSE or cache entries; 401/403/404 verified before access.|unstarted|
|N04|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M14.md](../assignments/M14.md)|Broker outage120s, consumer killed after DB commit beforeACK; pending saga reconciles ≤120s after recovery for 100 bookings; DLQ poison remains quarantined.|unstarted|
|N05|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M12.md](../assignments/M12.md)|100% synthetic test traces sampled; booking→outbox→consumer→PSP causality queryable; logs correlate; metrics have no booking/customer label.|unstarted|
|N06|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M14.md](../assignments/M14.md)|Lab SLO 99% successful eligible commands over 1h controlled run (denominator excludes auth/validation/conflict; includes dependency5xx). No claim about monthly production availability.|unstarted|
|N07|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M15.md](../assignments/M15.md)|TLS on ingress and internal production-like traffic, JWT issuer/audience/expiry checked, secrets absent repository/logs, least-privilege DB/broker roles; security scenario suite passes.|unstarted|
|N08|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M16.md](../assignments/M16.md)|Seven service images and DB migration streams; notification-only release changes no other digest; each service tests/builds/deploys without importing other business implementation.|unstarted|
|N09|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M11.md](../assignments/M11.md)|Keyboard complete customer checkout and operator return; visible focus; labels/errors; no color-only state; contrast normal text≥4.5:1; 360px without horizontal page scroll.|unstarted|
|N10|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M17.md](../assignments/M17.md)|Snapshot RPO target≤24h; measured isolated restore RTO≤30min for fixture dataset; reconnect mismatched service snapshots through reconcile, report unrecoverable delta.|unstarted|
|N11|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M15.md](../assignments/M15.md)|Synthetic users only; auth logs7d, telemetry7d, notifications30d, inbox/idempotency24h minimum with replay rules; booking/ledger retained for lab history; scrub demo emails on exports.|unstarted|
|N12|[requirements/nonfunctional.md](../requirements/nonfunctional.md)|[assignments/M18.md](../assignments/M18.md)|Clean lab host builds pinned images/contracts; bootstrap docs checked by reviewer; no mandatory external cloud, CDN or paid integration.|unstarted|
|A01|[reviews/engineering-audit.md](../reviews/engineering-audit.md)|[assignments/M18.md](../assignments/M18.md)|Audit gate row A01|unstarted|
|A02|[reviews/engineering-audit.md](../reviews/engineering-audit.md)|[assignments/M18.md](../assignments/M18.md)|Audit gate row A02|unstarted|
|A03|[reviews/engineering-audit.md](../reviews/engineering-audit.md)|[assignments/M18.md](../assignments/M18.md)|Audit gate row A03|unstarted|
|A04|[reviews/engineering-audit.md](../reviews/engineering-audit.md)|[assignments/M18.md](../assignments/M18.md)|Audit gate row A04|unstarted|
|A05|[reviews/engineering-audit.md](../reviews/engineering-audit.md)|[assignments/M18.md](../assignments/M18.md)|Audit gate row A05|unstarted|
|A06|[reviews/engineering-audit.md](../reviews/engineering-audit.md)|[assignments/M18.md](../assignments/M18.md)|Audit gate row A06|unstarted|
|A07|[reviews/engineering-audit.md](../reviews/engineering-audit.md)|[assignments/M18.md](../assignments/M18.md)|Audit gate row A07|unstarted|
|A08|[reviews/engineering-audit.md](../reviews/engineering-audit.md)|[assignments/M18.md](../assignments/M18.md)|Audit gate row A08|unstarted|
|A09|[reviews/engineering-audit.md](../reviews/engineering-audit.md)|[assignments/M18.md](../assignments/M18.md)|Audit gate row A09|unstarted|
|A10|[reviews/engineering-audit.md](../reviews/engineering-audit.md)|[assignments/M18.md](../assignments/M18.md)|Audit gate row A10|unstarted|
|A11|[reviews/engineering-audit.md](../reviews/engineering-audit.md)|[assignments/M18.md](../assignments/M18.md)|Audit gate row A11|unstarted|

## Original brief coverage

| ID | Requirement | Artifacts | Readiness |
|---|---|---|---|
|B01|Роль / самостоятельность|[README.md](../README.md), [assignments/M01.md](../assignments/M01.md)|Business implementation intentionally student-owned|
|B02|Исследование / выбор|[research/market-study.md](../research/market-study.md), [research/sources.json](../research/sources.json)|Primary sources checked; expired jobs explicit|
|B03|Реальные микросервисы|[architecture/system-design.md](../architecture/system-design.md), [architecture/services.json](../architecture/services.json)|7business owners, private DB, independent deployment criteria|
|B04|PRD / бизнес-логика / stories|[product/PRD.md](../product/PRD.md), [product/business-processes.md](../product/business-processes.md), [product/stories/F01.md](../product/stories/F01.md)|20full stories, precise states and acceptance|
|B05|System Design / contracts / distributed|[architecture/diagrams/index.json](../architecture/diagrams/index.json), [contracts/README.md](../contracts/README.md)|43rendered SVG, 7OpenAPI+7AsyncAPI, fault mechanisms|
|B06|Стек и глубина|[architecture/technology-decisions.md](../architecture/technology-decisions.md), [operations/fundamentals.md](../operations/fundamentals.md)|Problem/alternative/limit/practice/proof for17technology groups|
|B07|Учебные задания|[assignments/milestones.json](../assignments/milestones.json), [reviews/reviewer-guide.md](../reviews/reviewer-guide.md)|18docs with all required sections|
|B08|UI/UX|[design/prototype.html](../design/prototype.html), [design/design-spec.md](../design/design-spec.md), [design/screens.json](../design/screens.json)|22responsive screens; role/journey/state controls|
|B09|Интерактивный атлас / roadmap|[atlas/index.html](../atlas/index.html), [roadmaps/tracks.json](../roadmaps/tracks.json)|12sections,15visual dependency tracks, local progress/export|
|B10|Engineering process|[operations/engineering-process.md](../operations/engineering-process.md), [operations/templates/pull_request.md](../operations/templates/pull_request.md)|Templates, ADR, migration, release, rollback, runbooks|
|B11|Финальный результат / audit|[reviews/engineering-audit.md](../reviews/engineering-audit.md), [requirements/nonfunctional.md](../requirements/nonfunctional.md)|11audit gates and quantitative lab thresholds|
|B12|Файлы / архив / исходники|[PROJECT_INDEX.md](../PROJECT_INDEX.md), [tools/build_pack.py](../tools/build_pack.py), [exports/handbook.html](../exports/handbook.html)|Local first; ZIP excludes validator dependencies|
|B13|Quality / coverage|[reviews/pack-quality.md](../reviews/pack-quality.md), [reviews/coverage.json](../reviews/coverage.json)|Pack QA separate from future runtime evidence|
|B14|Фазы A–F|[reviews/phase-register.md](../reviews/phase-register.md)|Research/design/visual/assignments/packaging/audit recorded|
|B15|Учебный подход|[operations/fundamentals.md](../operations/fundamentals.md), [operations/engineering-process.md](../operations/engineering-process.md)|Explain→independent practice→review→errors→confirmation|
