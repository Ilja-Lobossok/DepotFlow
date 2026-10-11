# Runbook: dlq-replay

## Trigger / owner

DLQ count>0; implementing engineer, warehouse operator where physical action involved. Lab only.

## Diagnosis

Read schema error, consumer version, retry history; distinguish poison payload from outage. Preserve original event and metadata.

## Recovery

Fix compatible consumer or quarantine invalid schema. Replay one valid message original event_id, monitor then batch max20. Never generate fresh identity to bypass inbox.

## Verification / escalation

Inbox+effects single commit; no duplicate ledger/allocation; poison remains documented with owner.

Capture correlation, state snapshots from owners, UTC times and exact induced fault. If unverifiable leave incident open. See incident template; no force SQL status change across owners.
