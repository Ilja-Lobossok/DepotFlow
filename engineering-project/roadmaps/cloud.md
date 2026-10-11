# Cloud roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Local environment baseline — M01

Prerequisite: none.

Практика: Lab foundations. Evidence: One independent build per service; no shared DB role; dependency health evidence.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M01.md).

## 2. Trust/network topology — M15

Prerequisite: M14.

Практика: Production-like Kubernetes & security. Evidence: Old pods drain30s; own migration job; wrong DB role denied; rollout maintains invariants.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M15.md).

## 3. Plan/budget or local equivalent — M17

Prerequisite: M16.

Практика: IaC, backup & restore. Evidence: Second Ansible run unchanged; restore≤30min fixture, delta known; no credentials in state repo.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M17.md).

## 4. Defend failure domain — M18

Prerequisite: M17.

Практика: Engineering audit & architecture defense. Evidence: Every requirement evidence link resolves; reviewer independently runs critical races/recovery.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M18.md).
