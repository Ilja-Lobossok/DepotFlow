# Runbook: stuck-saga

## Trigger / owner

saga_pending_seconds>60; implementing engineer, warehouse operator where physical action involved. Lab only.

## Diagnosis

Find correlation in Booking timeline, trace Inventory/Billing commands and outbox age; query authoritative owner status by booking_id/provider_key.

## Recovery

If provider UNKNOWN query sandbox before any retry. Requeue original valid command ID after dependency healthy; never manual-set CONFIRMED.

## Verification / escalation

After recovery100 bookings finish or explicit manual_review within120s; no cancelled allocation/net captured. Escalate ambiguous handover to physical check.

Capture correlation, state snapshots from owners, UTC times and exact induced fault. If unverifiable leave incident open. See incident template; no force SQL status change across owners.
