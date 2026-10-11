# Environment and deployment specification

These are target designs; nothing provisioned by this assignment pack. Windows edits/viewing; Linux lab (WSL2 or isolated VM) is where future Docker/Kubernetes commands run. Do not modify current personal VMs or system settings without approval. Student measures available CPU/RAM first.

| Profile | Budget assumption | Topology | Purpose / limitation |
|---|---|---|---|
| lab-lite |4vCPU,8GB,20GB free|Compose subsets, JVM Xmx192m initially, DB instance separate owned DBs|First milestones; no full stack SLA benchmark|
| lab-standard |8vCPU,16GB,40GB free|7services, own DBs one Postgres node,1Rabbit,1Redis,Keycloak, telemetry|Fixed N01 load and restore fixture, no HA|
| lab-cluster |8vCPU,24GB,60GB free|kind/k3d3nodes, replicas2 core where needed,3Rabbit quorum, own DB credentials|Failure experiments; nodes share host failure domain|
| production-like |Same cluster or isolated VM|TLS, independent images, migration jobs, policies, backup target separate volume|Demonstrate operations; no production uptime claim|
| optional AWS |User authorized sandbox budget only|VPC private subnets, ingress VM/load balancer, storage, IAM, budget alarm|Live cloud requires measured cost/cleanup; not performed by author|

Requests starting values per JVM cpu100m/memory256Mi, limits cpu1/memory512Mi; Node100m/128Mi to1/256Mi. These values must be profiled, not assumed stable for chosen framework. DB/Rabbit/Keycloak needs separate limits and volume budgets; resource sum recorded, OOMKilled evidence changes settings. Startup probe every5s up to120s; readiness DB/pool every5s with3fail; liveness process every10s with3fail. Broker fault must not restart entire fleet. terminationGracePeriod30s, preStop stops command acceptance/consumers then drains transaction≤20s. pdb minAvailable1 only with2 replicas, not magic protection for one pod.

Ingress443 only; internal HTTP8080 over TLS production-like. Own DB5432, broker5671, Redis6379 TLS as supported/configured, OTel4317; admin ports only loopback in dev. Default deny in cluster, explicit connection matrix operations/network-security.md. Keycloak persisted independently, never share service DB users. Migrations per owner init/job before rollout; conflicting migration workers serialized. Persistent volumes require backups; StatefulSet doesn't supply DB replication automatically.

Compose design: networks edge, app, data, telemetry; only gateway connects edge/app, service joins app+own data, expose no DB/broker publicly. Compose networks not a strong per-service firewall; DB grants and OS/cluster policy provide real denial tests. Compose manifest is student deliverable M01; no pretend deploy YAML with missing application images shipped here.
