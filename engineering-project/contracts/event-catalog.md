# Event catalog

All commands/facts version1. Org/correlation always envelope; the payload table is exact required schema in data/events.

| Type | Owner | Consumers | Payload properties |
|---|---|---|---|
|membership.changed.v1|tenancy|external lab projection|membership_id, subject_id, role, status, depot_id|
|catalog.changed.v1|catalog|catalog|model_id, rate_version, active|
|booking.reserve-requested.v1|booking|inventory|booking_id, customer_id, quote, command_id, deadline_at|
|hold.created.v1|inventory|booking|booking_id, hold_id, asset_ids, expires_at|
|hold.rejected.v1|inventory|booking|booking_id, reason|
|hold.expired.v1|inventory|booking|booking_id, hold_id, expired_at|
|booking.commit-requested.v1|booking|inventory|booking_id, hold_id, intent_id, command_id|
|allocation.committed.v1|inventory|booking|booking_id, hold_id, asset_ids|
|booking.release-requested.v1|booking|inventory|booking_id, command_id, reason|
|allocation.released.v1|inventory|booking|booking_id, reason, tombstone|
|asset.unavailable.v1|inventory|booking, fulfillment|asset_id, reason, affected_booking_ids|
|billing.authorize-requested.v1|booking|billing|booking_id, customer_id, amount_minor, currency, command_id, deadline_at|
|payment.authorized.v1|billing|booking|booking_id, intent_id, authorized_minor, authorization_expires_at|
|payment.failed.v1|billing|booking|booking_id, intent_id, reason|
|billing.void-requested.v1|booking|billing|booking_id, command_id, reason|
|payment.voided.v1|billing|booking|booking_id, intent_id, operation_id, voided_minor, remaining_authorization_minor, kind|
|billing.settle-requested.v1|booking|billing|booking_id, intent_id, command_id, return_report_id, capture_minor, currency|
|payment.captured.v1|billing|booking|booking_id, intent_id, operation_id, captured_minor|
|payment.refunded.v1|billing|booking, notification|booking_id, intent_id, operation_id, refunded_minor, customer_id|
|booking.confirmed.v1|booking|fulfillment, notification|booking_id, customer_id, depot_id, asset_ids, quote|
|booking.cancelled.v1|booking|fulfillment, notification|booking_id, customer_id, reason|
|fulfillment.handed-over.v1|fulfillment|inventory, booking|booking_id, job_id, claim_id, asset_ids, handed_over_at|
|fulfillment.returned.v1|fulfillment|inventory, booking, notification|booking_id, job_id, return_report_id, asset_ids, customer_id, condition, damage_minor, late_days, returned_at|
