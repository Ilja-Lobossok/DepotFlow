# System Design roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Boundaries & ADR — M01

Prerequisite: none.

Практика: Lab foundations. Evidence: One independent build per service; no shared DB role; dependency health evidence.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M01.md).

## 2. Strong local invariants — M04

Prerequisite: M03.

Практика: Inventory integrity. Evidence: 100 simultaneous overlapping requests on one unit produce1hold; all-or-nothing qty5.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M04.md).

## 3. Eventual consistency costs — M08

Prerequisite: M07.

Практика: Cancellation & races. Evidence: 100 runs each race: no cancelled active allocation/net captured; completion≤120s after recovery.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M08.md).

## 4. Architecture defense — M18

Prerequisite: M17.

Практика: Engineering audit & architecture defense. Evidence: Every requirement evidence link resolves; reviewer independently runs critical races/recovery.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M18.md).
