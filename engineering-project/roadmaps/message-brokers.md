# Message Brokers roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Contracts — M05

Prerequisite: M04.

Практика: Booking commands & idempotency. Evidence: 20 repeats create1booking; different tenant same key works.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M05.md).

## 2. Rabbit confirms/ack — M06

Prerequisite: M05.

Практика: Messaging & contract gates. Evidence: At least10 duplicate deliveries yield one effect; poison schema→DLQ with original metadata.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M06.md).

## 3. Late events + DLQ — M08

Prerequisite: M07.

Практика: Cancellation & races. Evidence: 100 runs each race: no cancelled active allocation/net captured; completion≤120s after recovery.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M08.md).

## 4. Kafka compare/rebalance — M14

Prerequisite: M13.

Практика: Reliability & performance laboratory. Evidence: 20VU read p95≤300ms command≤500ms saga≤5s healthy; recovery100 bookings≤120s.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M14.md).
