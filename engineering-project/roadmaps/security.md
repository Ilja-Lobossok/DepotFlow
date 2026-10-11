# Security roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Tenant/role controls — M02

Prerequisite: M01.

Практика: Identity & tenant boundaries. Evidence: 401 invalid token;403 forbidden own command;404 foreign object; mutations revoke immediately.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M02.md).

## 2. Signed webhooks — M10

Prerequisite: M09.

Практика: Settlement & refunds. Evidence: 15000 auth example yields8500 capture; two full refunds never overrefund.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M10.md).

## 3. Dependency/supply chain — M13

Prerequisite: M12.

Практика: Contracts, migrations & CI. Evidence: Old consumer passes additive schema; breaking change blocked; previous migration upgrade works.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M13.md).

## 4. TLS/network attacks — M15

Prerequisite: M14.

Практика: Production-like Kubernetes & security. Evidence: Old pods drain30s; own migration job; wrong DB role denied; rollout maintains invariants.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M15.md).
