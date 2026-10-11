# Runbook: slow-api

## Trigger / owner

p95/error budget target exceeded; implementing engineer, warehouse operator where physical action involved. Lab only.

## Diagnosis

Trace gateway→Tenancy→owner DB, compare histogram and SQL buffers, queue/thread pool wait; inspect resource limits.

## Recovery

Remove accidental N+1 or missing index after measured query plan; set bounded pool/backpressure. Roll back regression image if threshold release gate met.

## Verification / escalation

Repeat same seed/workload/hardware, publish before/after and error denominator; do not average p95 values.

Capture correlation, state snapshots from owners, UTC times and exact induced fault. If unverifiable leave incident open. See incident template; no force SQL status change across owners.
