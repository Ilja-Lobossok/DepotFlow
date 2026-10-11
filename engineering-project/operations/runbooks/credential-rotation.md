# Runbook: credential-rotation

## Trigger / owner

expired TLS / scheduled principal rotation; implementing engineer, warehouse operator where physical action involved. Lab only.

## Diagnosis

Find scope affected, expiry, mounted version; redact secrets from report.

## Recovery

Create overlap credential, roll one caller, verify new access; revoke old; ensure own DB/broker grants preserved. Lab principal only.

## Verification / escalation

New accepted old rejected, no expanded privileges, app healthy; audit owner/time with no secret values.

Capture correlation, state snapshots from owners, UTC times and exact induced fault. If unverifiable leave incident open. See incident template; no force SQL status change across owners.
