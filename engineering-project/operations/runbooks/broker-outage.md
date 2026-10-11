# Runbook: broker-outage

## Trigger / owner

broker unavailable / oldest outbox>60s; implementing engineer, warehouse operator where physical action involved. Lab only.

## Diagnosis

Check socket/DNS/TLS/ACL and confirms; inspect outbox/inbox; healthy HTTP acceptance may leave pending.

## Recovery

Restore broker/topology, bounded backoff workers; publisher mandatory route confirms before marking. Scale consumers only after observing DB capacity.

## Verification / escalation

Drain backlog to0; compare all outbox effects, pending ages and deadline compensations; no mass pod restarts.

Capture correlation, state snapshots from owners, UTC times and exact induced fault. If unverifiable leave incident open. See incident template; no force SQL status change across owners.
