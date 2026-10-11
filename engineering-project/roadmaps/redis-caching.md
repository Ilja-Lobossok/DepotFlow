# Redis & Caching roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Authoritative quote first — M03

Prerequisite: M02.

Практика: Catalog & pricing. Evidence: 25h quote calculates10000 rental+20000 deposit; expired quote422.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M03.md).

## 2. Cache-aside + invalidation — M11

Prerequisite: M10.

Практика: Product frontend & notifications. Evidence: 360px no page overflow; duplicate fact one notification; fresh quote bypasses cache.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M11.md).

## 3. Eviction/outage experiment — M14

Prerequisite: M13.

Практика: Reliability & performance laboratory. Evidence: 20VU read p95≤300ms command≤500ms saga≤5s healthy; recovery100 bookings≤120s.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M14.md).

## 4. Bounded production config — M15

Prerequisite: M14.

Практика: Production-like Kubernetes & security. Evidence: Old pods drain30s; own migration job; wrong DB role denied; rollout maintains invariants.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M15.md).
