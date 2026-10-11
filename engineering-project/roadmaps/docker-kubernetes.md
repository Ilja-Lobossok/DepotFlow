# Docker & Kubernetes roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Images/volumes — M01

Prerequisite: none.

Практика: Lab foundations. Evidence: One independent build per service; no shared DB role; dependency health evidence.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M01.md).

## 2. Independent builds — M13

Prerequisite: M12.

Практика: Contracts, migrations & CI. Evidence: Old consumer passes additive schema; breaking change blocked; previous migration upgrade works.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M13.md).

## 3. Probes/limits — M15

Prerequisite: M14.

Практика: Production-like Kubernetes & security. Evidence: Old pods drain30s; own migration job; wrong DB role denied; rollout maintains invariants.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M15.md).

## 4. Rollout/rollback — M16

Prerequisite: M15.

Практика: Independent delivery & rollback. Evidence: Notification-only diff; failed update leaves working pods; revert image retains schema compatibility.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M16.md).
