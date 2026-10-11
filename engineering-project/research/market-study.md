# Research & product selection — 11 October 2026

Дата проверки: 2026-10-11, Europe/Tallinn. Метод: целевая качественная выборка страниц работодателей и официальной документации. Это не перепись вакансий и не статистика долей рынка. Поиск смещён к Java, TypeScript и platform; результаты не доказывают превосходство языка или вероятность трудоустройства. География, разрешение на работу, язык и образование требуют отдельной проверки при реальном отклике.

## Наблюдения и выводы

R01 показывает ценность фундаментальных знаний и объяснения решений. R02–R06 дают основания тренировать JVM, SQL, API, review и frontend; senior-позиции используются только как ориентир роста. R07–R09 показывают отдельный путь platform: Linux, сети, IaC, контейнеры, инциденты. Название Junior иногда соседствует с требованием 2 лет, поэтому диплом проекта не равен опыту работы. R10 исключена как закрытая страница. Малое число локальных entry-level находок нельзя трактовать как отсутствие спроса.

Главный учебный результат: объяснимые транзакции, контракт API, диагностика сбоя и воспроизводимый deployment. Количество логотипов инструментов не является результатом. Java/Spring выбирается для core-domain; React/TypeScript — для UI; один TypeScript Notification сервис даёт межъязыковую контрактную практику. Kafka не добавляется в основную систему: RabbitMQ лучше соответствует командам и ограниченной нагрузке, Kafka изучается в сравнительной лаборатории.

## Сравнение предметных областей

Оценки 1–5 — авторское суждение, не измерения рынка. Критерии: коммерческий реализм (C), естественные границы (M), распределённость (D), бизнес-правила (B), четыре направления (E), соответствие задачам вакансий (J), выполнимость одному (S), защита (I). Вес каждого одинаковый; сумма не скрывает trade-offs.

| Вариант | C | M | D | B | E | J | S | I | Итог /40 | Ограничение |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| DepotFlow: B2B аренда оборудования |5|5|5|5|5|4|4|5|38|Временные интервалы и физический возврат усложняют тесты|
| ColdRoute: холодовая логистика |5|5|5|5|5|4|2|5|36|Телеметрия и маршрутизация быстро расширяют scope|
| PermitDesk: разрешения на строительство |5|3|3|5|4|4|4|4|32|Много workflow, меньше естественных конкурентных ресурсов|
| SeatWave: билеты на мероприятия |5|4|5|4|5|4|4|4|35|Хорошая конкуренция, но предметная область часто повторяет учебные проекты|

Выбран DepotFlow: ограниченные физические ресурсы, срок удержания, необратимая выдача и отдельно управляемые платежи дают разные причины распределённости. Это вымышленный продукт с реалистичными правилами, а не утверждение о внутренней архитектуре существующей компании. Для маленького коммерческого стартапа монолит мог бы стоить меньше; здесь микросервисы — явная цель capstone, а границы выбраны по ответственности, а не ради контейнеров.

Исключены: Match Me, marketplace между независимыми арендодателями, реальная обработка карт, налоги по странам, бухгалтерская сертификация, оптимизация маршрутов, IoT. Sandbox PSP и почтовый sink обязательны; настоящие деньги и персональные данные не нужны.

## Источники и состояние

### R01 — Wise Graduate Software Engineer

Tallinn; graduate. Expired explicitly; cohort September 2026.

CS fundamentals, major programming language, review, communication. Language list is not a mandatory stack.

Источник: [Wise Graduate Software Engineer](https://wise.jobs/job/graduate-software-engineer-in-tallinn-jid-2903). Проверено 2026-10-11.

### R02 — Wise API Experience Java

Europe; senior reference. Accessible posting; older indexed page, hiring status unconfirmed.

Java/Spring Boot, public APIs, microservices, events, relational data, Kafka or similar. Senior expectations are a future depth reference.

Источник: [Wise API Experience Java](https://jobs.smartrecruiters.com/Wise/744000063454628-senior-software-engineer-i-api-experience-java). Проверено 2026-10-11.

### R03 — Bolt Engineering careers

Tallinn; senior reference. Accessible employer careers page.

Node.js/TypeScript, distributed systems and product algorithms; reinforces transferability, not a junior hiring guarantee.

Источник: [Bolt Engineering careers](https://bolt.eu/en/careers/teams/engineering/). Проверено 2026-10-11.

### R04 — Codeborne full-stack developer

Tallinn; mid-senior. Accessible employer posting.

Java/Kotlin or Svelte/Vue, TDD, pair work, client communication. React is not universal.

Источник: [Codeborne full-stack developer](https://codeborne.com/en/jobs/full-stack-developer-tallinn/). Проверено 2026-10-11.

### R05 — Tipico (Junior) Java Developer

Europe; junior. Indexed employer posting; availability unconfirmed.

Java backend, React frontend, first practical experience, review and end-to-end ownership.

Источник: [Tipico (Junior) Java Developer](https://jobs.smartrecruiters.com/Tipico/744000136171599--junior-java-developer-m-f-x-?trid=7d1dcdfa-96a8-4e55-bb9c-0db211f5a9b3). Проверено 2026-10-11.

### R06 — Version 1 Junior Java Developer

UK; junior title, 2 years required. Accessible posting.

Java APIs, Spring, Git, Maven, Jenkins, Azure desirable. Junior title does not mean zero experience.

Источник: [Version 1 Junior Java Developer](https://jobs.smartrecruiters.com/Version1/744000148946885-junior-java-developer). Проверено 2026-10-11.

### R07 — LOGEX Junior Platform Engineer

Amsterdam; junior title, around 2 years. Accessible older indexed posting; availability unconfirmed.

K8s/K3s, Linux, Terraform/Ansible, cloud. Platform work combines troubleshooting and delivery.

Источник: [LOGEX Junior Platform Engineer](https://logex.recruitee.com/o/platform-engineer-1?lang=en). Проверено 2026-10-11.

### R08 — SEB Junior Software Platform Engineer

Solna; graduate/early career. Accessible; deadline 2026-11-01 stated.

CI/CD, testing, containers, IaC. Prior platform employment not required; listed tools are advantages, not all mandatory.

Источник: [SEB Junior Software Platform Engineer](https://jobs.eu.lever.co/seb/3ae41077-3709-4376-b54f-b47ab3af01b8). Проверено 2026-10-11.

### R09 — Capgemini Junior Cloud Engineer

Porto; junior title. Indexed employer posting.

Cloud, IaC, Linux, networking, containers and incident analysis; requirements include strong experience despite title.

Источник: [Capgemini Junior Cloud Engineer](https://careers.capgemini.com/job/Vila-Nova-de-Gaia-Junior-Platform-Engineer-%28Porto%29/1399964033/?feedId=388633&tcsource=apply). Проверено 2026-10-11.

### R10 — Evolution React openings

Tallinn; mid-senior. Direct fetch 410 Gone; excluded from active evidence.

Search snippet mentions React/TypeScript and delivery tooling; retained as a negative freshness check only.

Источник: [Evolution React openings](https://careers.evolution.com/job/744000126042610/). Проверено 2026-10-11.

### E01 — Zalando: Simplicity by Distributing Complexity

Engineering; 2018-01-23. Article read.

Independent data ownership and derived views illustrate the costs of event driven data aggregation. Not a blueprint for this domain.

Источник: [Zalando: Simplicity by Distributing Complexity](https://engineering.zalando.com/posts/2018/01/simplicity-by-distributing-complexity.html). Проверено 2026-10-11.

### D01 — PostgreSQL range types

Official documentation. Read; page resolves to PostgreSQL 18.

Range exclusion can prevent overlapping allocations; design exercise uses this invariant.

Источник: [PostgreSQL range types](https://www.postgresql.org/docs/current/rangetypes.html). Проверено 2026-10-11.

### D02 — RabbitMQ confirms

Official documentation. Read.

Publisher confirms and consumer acknowledgements are separate; they do not guarantee business exactly-once.

Источник: [RabbitMQ confirms](https://www.rabbitmq.com/docs/confirms). Проверено 2026-10-11.

### D03 — RabbitMQ reliability

Official documentation. Read.

Connection loss may cause redelivery; consumers must tolerate duplicates.

Источник: [RabbitMQ reliability](https://www.rabbitmq.com/docs/reliability). Проверено 2026-10-11.

### D04 — Kubernetes probes

Official documentation. Read.

Startup, readiness and liveness serve different purposes; do not restart the fleet for broker failure.

Источник: [Kubernetes probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/). Проверено 2026-10-11.

### D05 — OpenTelemetry traces

Official documentation. Read.

Trace/span context connects causal work across services.

Источник: [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/). Проверено 2026-10-11.

### D06 — Spring Boot requirements

Official documentation. Read.

Choose Java 21 and Boot 4.1 family, verify compatible libraries and pin exact patch at M01.

Источник: [Spring Boot requirements](https://docs.spring.io/spring-boot/system-requirements.html). Проверено 2026-10-11.

### D07 — OpenAPI 3.1.1

Specification. Read.

Machine-readable HTTP contracts, JSON Schema data descriptions.

Источник: [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html). Проверено 2026-10-11.

### D08 — AsyncAPI 3.0

Specification. Read.

Per-application send/receive contracts; channels do not by themselves define queue topology.

Источник: [AsyncAPI 3.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0). Проверено 2026-10-11.

### D09 — Keycloak OIDC

Official documentation. Read.

OIDC provider separates authentication from application membership authorization.

Источник: [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers). Проверено 2026-10-11.
