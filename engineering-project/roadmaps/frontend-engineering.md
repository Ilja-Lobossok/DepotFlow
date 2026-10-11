# Frontend Engineering roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Auth/access routes — M02

Prerequisite: M01.

Практика: Identity & tenant boundaries. Evidence: 401 invalid token;403 forbidden own command;404 foreign object; mutations revoke immediately.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M02.md).

## 2. Pending server state — M05

Prerequisite: M04.

Практика: Booking commands & idempotency. Evidence: 20 repeats create1booking; different tenant same key works.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M05.md).

## 3. Warehouse forms — M09

Prerequisite: M08.

Практика: Warehouse physical workflow. Evidence: Cancel/handover exactly one winner; double return one report; absent asset not handed over.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M09.md).

## 4. Accessible E2E — M11

Prerequisite: M10.

Практика: Product frontend & notifications. Evidence: 360px no page overflow; duplicate fact one notification; fresh quote bypasses cache.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M11.md).
