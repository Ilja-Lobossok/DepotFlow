# Technology map

Core stack is selected, not everything listed is installed. Jenkins, gRPC, Kafka are comparative labs; service mesh, Redis Streams, BullMQ are evaluated alternatives, no mandatory installation. Version locks recorded by student M01; this pack includes no running backend.

## Java21 + Spring Boot

**Problem:** Типизированные domain rules, transactions/security. **Decision:** use in Backend. **Alternatives:** Node/Nest, .NET, Go. **Limits:** JVM memory and library compatibility; pin Boot4.1 patch.

**Study:** HTTP lifecycle, DI, JDBC transaction boundary. **Practice result:** M03 quote API and unit/integration suite. **Understanding check:** Explain rollback when exception is swallowed.

## REST / OpenAPI

**Problem:** Явные HTTP contracts. **Decision:** use in Backend. **Alternatives:** gRPC/protobuf lab. **Limits:** No streaming optimization; breaking semantics need version.

**Study:** status codes, caching, deadlines, idempotency. **Practice result:** M06 generated fixtures/provider checks. **Understanding check:** Explain why POST timeout does not mean failure.

## React / TypeScript

**Problem:** Accessible role-based UI and server-state handling. **Decision:** use in Frontend. **Alternatives:** Vue/Svelte. **Limits:** UI types do not validate network at runtime.

**Study:** router, TanStack Query, forms, runtime validation. **Practice result:** M11 checkout and operator E2E. **Understanding check:** Distinguish UI optimistic cache from booking authority.

## PostgreSQL / Flyway

**Problem:** Owned durable aggregates and interval integrity. **Decision:** use in Databases. **Alternatives:** MySQL; ORM; Liquibase. **Limits:** Physical instance shared dev still has one failure domain.

**Study:** SQL, MVCC, locks, exclusion, plans, migration. **Practice result:** M04 contention and query evidence. **Understanding check:** Explain write skew and why Redis lock is insufficient.

## Redis

**Problem:** Bounded catalog cache and gateway throttling. **Decision:** use in Caching. **Alternatives:** in-process, HTTP ETag; no cache. **Limits:** Eviction and stale data; never inventory truth.

**Study:** TTL, memory max, noeviction vs allkeys-lru, persistence. **Practice result:** M11 cache outage/rebuild lab. **Understanding check:** Prove stale cache cannot change quote price.

## RabbitMQ

**Problem:** Durable routed commands/events, DLQ. **Decision:** use in Messaging. **Alternatives:** Kafka lab; Redis Streams; BullMQ. **Limits:** Queue topology and confirms need explicit ops.

**Study:** acks, confirms, routing, prefetch, quorum. **Practice result:** M06 outbox/inbox crash replay. **Understanding check:** Explain confirm success without consumer business effect.

## Kafka comparative lab

**Problem:** Replayable depot utilization projection. **Decision:** use in Messaging. **Alternatives:** RabbitMQ append-only event archive. **Limits:** Not installed core; partitions and rebalance costs.

**Study:** offsets, key ordering, retention, group rebalances. **Practice result:** M14 comparative failure report. **Understanding check:** Explain ordering per key vs global ordering.

## Keycloak / OIDC

**Problem:** Authentication without home-made password flow. **Decision:** use in Security. **Alternatives:** managed IdP; session BFF. **Limits:** IdP availability and token revocation semantics.

**Study:** PKCE, JWKS rotation, JWT audience, RBAC. **Practice result:** M02 two tenants and revoke role. **Understanding check:** Explain authentication vs membership authorization.

## Linux / DNS / TLS / Nginx

**Problem:** Runtime process/network and edge routing. **Decision:** use in Linux. **Alternatives:** Caddy, Traefik. **Limits:** Need operational skills, not host security changes here.

**Study:** users, signals, sockets, DNS, certificates. **Practice result:** M01 lab and M15 network packet evidence. **Understanding check:** Explain DNS failure vs HTTP503 vs connection refused.

## Docker / Compose

**Problem:** Repeatable local dependencies and images. **Decision:** use in Containers. **Alternatives:** Podman. **Limits:** Volumes consume disk; Compose not HA.

**Study:** layers, nonroot, networks, bind/volume, health. **Practice result:** M01 immutable image and clean environment. **Understanding check:** Explain restart vs recreation vs lost volume.

## Kubernetes / Helm

**Problem:** Independent deployments, probes and rollback. **Decision:** use in Containers. **Alternatives:** Compose on VM; Nomad. **Limits:** Cluster overhead; DB HA not supplied by StatefulSet.

**Study:** requests/limits, services, rollout, policies, storage. **Practice result:** M15 kind/k3d deployment report. **Understanding check:** Explain readiness vs liveness with broker down.

## GitHub Actions

**Problem:** Repeatable changed-service checks and deploy. **Decision:** use in Delivery. **Alternatives:** GitLab CI; Jenkins lab. **Limits:** Remote runner costs/permissions, local fallback scripts.

**Study:** DAG, caches, artifacts, OIDC, environment gates. **Practice result:** M16 service-specific release and rollback. **Understanding check:** Explain why path filter can miss shared contract changes.

## OpenTofu / Ansible

**Problem:** Cloud resource state + repeatable VM configuration. **Decision:** use in IaC. **Alternatives:** Terraform; cloud-native IaC. **Limits:** State secrets/lock, billing; Ansible not resource graph.

**Study:** plan/state/drift; idempotent playbooks. **Practice result:** M17 sandbox plan and local VM convergence. **Understanding check:** Explain IaC state vs actual resources and second run.

## AWS optional sandbox

**Problem:** VPC/IAM/storage and cost reasoning. **Decision:** use in Cloud. **Alternatives:** Azure/GCP; mandatory local equivalent. **Limits:** Real account optional and spending approval required.

**Study:** subnets, IAM, budgets, destroy, quotas. **Practice result:** M17 local simulation or authorized sandbox report. **Understanding check:** Explain single VM production-like single failure point.

## OpenTelemetry / Prometheus / Grafana / Loki / Tempo

**Problem:** Trace slow saga with metrics and logs. **Decision:** use in Observability. **Alternatives:** Jaeger, ELK. **Limits:** Storage/label cardinality cost; sampling changes visibility.

**Study:** trace context, histograms, exemplars, alerts. **Practice result:** M12 diagnose poisoned event with correlation. **Understanding check:** Find trace across async edge without logging JWT.

## JUnit / Testcontainers / Playwright / k6 / ZAP

**Problem:** Verify real transactions, UI, load and access attacks. **Decision:** use in Testing. **Alternatives:** Vitest, Gatling, Locust. **Limits:** Tests consume resources; synthetic fixture only.

**Study:** test levels, fault injection, percentiles, attack scope. **Practice result:** M14 reproducible failure/performance evidence. **Understanding check:** Explain why 100% line coverage does not prove invariants.

## ADRs / threat model / contract review

**Problem:** Document costs and reversible decisions. **Decision:** use in System Design. **Alternatives:** design review notes. **Limits:** Documentation must track actual change.

**Study:** ownership, consistency, recovery, architecture audit. **Practice result:** M18 defend failure decisions. **Understanding check:** Explain where strong consistency ends and manual review begins.
