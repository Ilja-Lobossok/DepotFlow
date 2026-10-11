# Backend Engineering roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. HTTP/JVM fundamentals — M01

Prerequisite: none.

Практика: Lab foundations. Evidence: One independent build per service; no shared DB role; dependency health evidence.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M01.md).

## 2. Неизменяемая котировка — M03

Prerequisite: M02.

Практика: Catalog & pricing. Evidence: 25h quote calculates10000 rental+20000 deposit; expired quote422.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M03.md).

## 3. Durable commands — M05

Prerequisite: M04.

Практика: Booking commands & idempotency. Evidence: 20 repeats create1booking; different tenant same key works.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M05.md).

## 4. Saga + sandbox adapter — M07

Prerequisite: M06.

Практика: Sandbox billing & confirmation saga. Evidence: Unknown reconciled by same key; expired hold never committed; one auth.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M07.md).
