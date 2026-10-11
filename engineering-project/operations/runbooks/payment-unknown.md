# Runbook: payment-unknown

## Trigger / owner

payment_unknown_total>0; implementing engineer, warehouse operator where physical action involved. Lab only.

## Diagnosis

Lookup intent operation and provider_key; inspect signed webhook history and trace masked transport error.

## Recovery

Query provider exact same key; persist capture/void/refund independently. Missing response is not decline. Manual review if provider result irreconcilable.

## Verification / escalation

Provider net and ledger net match; total captured≤auth and refund≤capture incl pending; no new charge key.

Capture correlation, state snapshots from owners, UTC times and exact induced fault. If unverifiable leave incident open. See incident template; no force SQL status change across owners.
