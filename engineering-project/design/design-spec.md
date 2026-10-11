# Product design specification — DepotFlow

Visual prototype: design/prototype.html; entirely offline, synthetic data and simulated state. It is a reference for independent React implementation, not the backend. Screens mapped in screens.json to F/M IDs. Editable HTML/CSS/JS source and rendered SVG architecture diagrams supplied; Figma unnecessary.

## Information architecture / journeys

Customer: catalog → availability → quote → checkout → pending → booking detail → cancel or settlement; notifications accessible from header. Operator: warehouse jobs → handover inspection → return → fleet/quarantine → maintenance. Finance: payment list → ledger → refund/manual review. Admin: team → role/depot assignment → catalog/rates → audit. Login/denied common. Role selector is a demonstration control, not authentication. Switch to role before screen; permissions enforced later in API.

## Design system

Palette: canvas#f4f6f7, ink#132a39, muted#526570, border#d4dfe4, brand#075d64, accent#b45512, danger#b42318, surface#ffffff, focus#1d70b8. Typography system Segoe UI/Arial offline; body16px line1.55, headings32/24/18px; tabular money/numbers. Spacing4/8/12/16/24/32; radius12 cards,8inputs/buttons; max content1240px; desktop sidebar232px + fluid main; mobile bottom-friendly full-width actions, single column≤720px. Customer forms put price/status alongside desktop, below on mobile; sticky summary never hides field focus.

Components: labeled text/date/qty/money field + help/error IDs; button primary/secondary/danger/loading disabled; breadcrumb; badge with text; table with header/empty/loading pagination; filter bar; status timeline; confirmation dialog; alert role/status aria-live; accessible tabs; progress indicator; notification card; code/correlation ID; responsive asset checklist. Dialog traps focus/escape closes and restores trigger in student implementation. Prototype uses inline review/confirm screen instead of inaccessible faux modal.

## State specification

Loading: skeleton or labeled progress, preserve layout, no duplicate submit. Empty: catalog suggests clear filters; warehouse says no pending jobs, no fake success. Error: stable problem code, correlation and retry safe only per operation ID. Unauthorized: login action401; denied403 explains required role/depot without foreign data. Quote expired: refresh and compare changed amount, requires user consent. Pending: outcome unknown, no success badge; manual review has explanation and contact operator. Success: confirmed only on allocation+auth proof; refund pending until authoritative event. Offline/SSE stale: updated_at banner plus snapshot recovery, never replay checkout automatically.

Accessibility target N09: WCAG-oriented keyboard journeys, explicit labels/errors, visible focus, no color-only statuses, text contrast≥4.5:1, reduced motion; touch targets≥44px. Implementation audit checks real assistive behavior; prototype visual QA is not certification. Tables scroll within region on narrow screens, no document horizontal overflow. Notification includes textual changed state rather than animation.

Screen / acceptance mapping screens.json; prototype controls navigate all screens and demonstrate loading/empty/error/success/denied/reconnecting. Prices/entities labeled demo; sample booking confirmed only by explicit simulated advance action. Persistent project progress belongs atlas, not business state. No forms send network requests.
