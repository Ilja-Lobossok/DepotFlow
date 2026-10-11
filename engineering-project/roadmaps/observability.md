# Observability roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Correlation IDs — M05

Prerequisite: M04.

Практика: Booking commands & idempotency. Evidence: 20 repeats create1booking; different tenant same key works.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M05.md).

## 2. Async trace context — M06

Prerequisite: M05.

Практика: Messaging & contract gates. Evidence: At least10 duplicate deliveries yield one effect; poison schema→DLQ with original metadata.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M06.md).

## 3. Dashboards/alerts — M12

Prerequisite: M11.

Практика: Observability & incident diagnosis. Evidence: Trace links across all saga edges; no high-cardinality booking metric label.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M12.md).

## 4. Incident & SLO evidence — M14

Prerequisite: M13.

Практика: Reliability & performance laboratory. Evidence: 20VU read p95≤300ms command≤500ms saga≤5s healthy; recovery100 bookings≤120s.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M14.md).
