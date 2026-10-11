# Databases roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Модель/migration — M03

Prerequisite: M02.

Практика: Catalog & pricing. Evidence: 25h quote calculates10000 rental+20000 deposit; expired quote422.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M03.md).

## 2. Locks & plans — M04

Prerequisite: M03.

Практика: Inventory integrity. Evidence: 100 simultaneous overlapping requests on one unit produce1hold; all-or-nothing qty5.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M04.md).

## 3. Ledger invariants — M10

Prerequisite: M09.

Практика: Settlement & refunds. Evidence: 15000 auth example yields8500 capture; two full refunds never overrefund.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M10.md).

## 4. Restore verification — M17

Prerequisite: M16.

Практика: IaC, backup & restore. Evidence: Second Ansible run unchanged; restore≤30min fixture, delta known; no credentials in state repo.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M17.md).
