# Testing Performance Reliability roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Pure vs integration — M03

Prerequisite: M02.

Практика: Catalog & pricing. Evidence: 25h quote calculates10000 rental+20000 deposit; expired quote422.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M03.md).

## 2. Contract/crash testing — M06

Prerequisite: M05.

Практика: Messaging & contract gates. Evidence: At least10 duplicate deliveries yield one effect; poison schema→DLQ with original metadata.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M06.md).

## 3. Load+fault experiments — M14

Prerequisite: M13.

Практика: Reliability & performance laboratory. Evidence: 20VU read p95≤300ms command≤500ms saga≤5s healthy; recovery100 bookings≤120s.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M14.md).

## 4. Timed recovery — M17

Prerequisite: M16.

Практика: IaC, backup & restore. Evidence: Second Ansible run unchanged; restore≤30min fixture, delta known; no credentials in state repo.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M17.md).
