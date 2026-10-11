# Final Engineering Audit — M18

Audit packet: commit/digests, exact lab profile, coverage ledger, contracts, ADRs, environment manifest and raw tests. Independent reviewer executes; this assignment pack has not run the future business tests. Mandatory gates below are all required, not points averaged into pass.

| Gate | Scenario | Pass evidence |
|---|---|---|
| A01 Product |quote→confirmed→handover→damaged return→settle→refund plus cancel|F01–F16 endpoint/UI/state evidence; exact money example|
| A02 Integrity |100reserve contenders, cancel/claim, duplicate/refund,lateauth|N02 zero invalid allocations/money changes; deterministic repeat100times|
| A03 Microservices |own DB grants,builds,images,migrations,contracts|seven independent business boundaries; foreign SQL denies; F19 release scopes|
| A04 Sync/async |quote GET and claim; AMQP reserve/facts|trace and broker effects; outbox/inbox crash recovery|
| A05 Delivery |additive contract, old consumer, roll/rollback|F17/F19 CI real assertions; expanded schema rollback|
| A06 Security |two tenants,role revoke,invalid token/webhook,policy denial|N03/N07 no cross-owner data/credentials|
| A07 Reliability |broker120s,PSPunknown,poison DLQ,missing contexts|N04/N05 recover within target or visible manualreview; no invented success|
| A08 Performance |fixed 20VU workload,3runs,raw samples|N01/N06 measured thresholds and eligible error denominator|
| A09 Recovery |isolated backup restore+PSPreconcile|N10 measured RTO≤30min/RPO≤24h and known checkpoint counts|
| A10 Reproducibility |fresh lab install,role UIs keyboard360px|N09/N12 clean start and no mandatory cloud/CDN|
| A11 Defense |random fault diagnosis≤15min, ownership trade-offs|student explains decisions,limitations and response-loss ambiguity|

Demo (~60–90min planning assumption):10min topology/ownership,15min core business,15min races/faults,10min release/restore summary then independent replay,15min troubleshooting and security,15min design questions. Full load/restore may run outside demo but raw evidence must be reproducible. Reviewer picks at least one fault not disclosed in advance. Code inspection focuses locks, inbox/outbox commit, provider adapter and authorization, not formatting.

Final verdict: ACCEPTED only all gates pass and no open integrity/security blockers; CONDITIONAL only for explicitly optional limitations; FAILED for any mandatory unverified gate. Ledger starts unimplemented. Include portfolio narrative that distinguishes personal capstone from employed production operations; cite measured lab results with profile.
