# CI-CD & IaC roadmap

Последовательность — зависимости, не даты. Глобальные prerequisites этапов сохраняются: нельзя выполнять только выбранную дорожку в обход других.

## 1. Git/reproducibility — M01

Prerequisite: none.

Практика: Lab foundations. Evidence: One independent build per service; no shared DB role; dependency health evidence.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M01.md).

## 2. Check DAG — M13

Prerequisite: M12.

Практика: Contracts, migrations & CI. Evidence: Old consumer passes additive schema; breaking change blocked; previous migration upgrade works.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M13.md).

## 3. Per-service release — M16

Prerequisite: M15.

Практика: Independent delivery & rollback. Evidence: Notification-only diff; failed update leaves working pods; revert image retains schema compatibility.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M16.md).

## 4. State/drift/convergence — M17

Prerequisite: M16.

Практика: IaC, backup & restore. Evidence: Second Ansible run unchanged; restore≤30min fixture, delta known; no credentials in state repo.

Проверка понимания: объяснить собственную реализацию и воспроизвести failure case этапа без подсказки. [Задание](../assignments/M17.md).
