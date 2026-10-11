# Runbook: asset-overrun

## Trigger / owner

past-end IN_USE / asset.unavailable; implementing engineer, warehouse operator where physical action involved. Lab only.

## Diagnosis

Check physical handover, scheduled end, return report and future commitments; identify impacted depots/bookings.

## Recovery

Mark asset unavailable and block handover, notify dispatcher. Resolve manually with cancel+compensation or documented advanced replacement; do not erase future allocations.

## Verification / escalation

Every impacted job has blocked/compensated or substituted evidence; no absent asset handed over.

Capture correlation, state snapshots from owners, UTC times and exact induced fault. If unverifiable leave incident open. See incident template; no force SQL status change across owners.
