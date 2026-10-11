# Linux & Networking roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Processes/sockets/DNS — M01

Prerequisite: none.

Практика: Lab foundations. Evidence: One independent build per service; no shared DB role; dependency health evidence.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M01.md).

## 2. TLS/auth — M02

Prerequisite: M01.

Практика: Identity & tenant boundaries. Evidence: 401 invalid token;403 forbidden own command;404 foreign object; mutations revoke immediately.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M02.md).

## 3. Trace network failure — M12

Prerequisite: M11.

Практика: Observability & incident diagnosis. Evidence: Trace links across all saga edges; no high-cardinality booking metric label.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M12.md).

## 4. Network policies — M15

Prerequisite: M14.

Практика: Production-like Kubernetes & security. Evidence: Old pods drain30s; own migration job; wrong DB role denied; rollout maintains invariants.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M15.md).
