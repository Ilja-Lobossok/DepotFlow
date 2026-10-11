# Allowed connections / threat model

| Caller | Destination | Protocol | Authorization |
|---|---|---|---|
| Browser | gateway / IdP |HTTPS443|PKCE, user access token in memory; CSP, strict CORS, no secrets in browser|
| gateway |7HTTP services|HTTPS internal|JWT forwarded; gateway strips spoofed X-Org/X-User|
| every service |Tenancy membership, Keycloak JWKS|HTTPS|scoped service identity + original subject; issuer/audience validated|
| Booking |Catalog quote lookup, Inventory/Billing status|HTTPS|booking service scope plus tenant|
| Fulfillment |Booking claim/status|HTTPS|fulfillment scope plus operator/depot|
| Tenancy |Inventory depot lookup|HTTPS|tenancy scope plus org|
| each service |own Postgres only|TLS5432|own app role; DDL migration role separate|
| event services |RabbitMQ|AMQPS5671|per-service ACL, commands address owner|
| Catalog/gateway |Redis|TLS6379|named ACL prefixes; no auth source|
| Billing |sandbox PSP|HTTPS|secret, provider idempotency key, signed callbacks|
| Notification |mail sink|SMTP internal|synthetic recipient; stable Message-ID|
| services |OTel collector|gRPC/HTTPS4317|internal identity; PII filter|
| collectors |Prometheus/Loki/Tempo|internal|no public dashboards without operator auth|

Default deny elsewhere. No cross-owner SQL, no direct client DB/broker, no management ingress on public network. TLS cert rotation exercise; service credentials have distinct audiences/scopes and network source alone does not authorize command.

Threats and tests: object authorization(IDOR)→two-tenant endpoint/event/SSE suite N03; role revocation→authoritative command check F01; forged tenant headers→gateway strip plus server derivation; forged PSP callback→HMAC timestamp within5min constant-time verification, unique provider_event_id; replay older signed callback→idempotency not duplicate money; SSRF→no user-controlled outbound URL; SQLi→parameterized queries; XSS→text output and CSP, no unsafe HTML user content; log leakage→scan token-like fixtures; resource exhaustion→body max64KB, per-org rate limits (20read/s,5command/s baseline), bounded thread/consumer pools; dependency attack→lockfile/SBOM/scan and signature/digest review.

TLS certificates/secrets in mounted file or secret store, not ConfigMap; rotate one principal at time with overlap, prove old revoked. Access token short-lived5min, no JWT/email in localStorage/logs. Frontend runtime auth remains memory; refresh via secure approach documented by student (BFF HttpOnly SameSite or IdP flow); prototype uses no authentication and is labeled as demonstration. Minimal synthetic data retention N11; legal compliance of a real business is out of scope, not asserted.

Additional allowed sync edge: Fulfillment → Inventory handover-check HTTPS, scope fulfillment and original operator/depot; failure blocks physical transfer.
