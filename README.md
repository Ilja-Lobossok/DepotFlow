# DepotFlow — Microservices Engineering Capstone

Полный комплект задания для самостоятельной разработки B2B-платформы аренды оборудования. 7 бизнес-сервисов, 18 инженерных этапов, 119 документов, 43 SVG-диаграммы, 22 экрана UI-прототипа, 15 дорожных карт, OpenAPI/AsyncAPI и схемы событий.

**Это спецификация, учебные задания и работающий локальный UI-прототип. Бизнес-backend пока не реализован.** При оценке отличайте качество проектного задания от доказательств работоспособности будущей распределённой системы.

## Скачать и открыть

- [Полный ZIP](DepotFlow-engineering-project.zip) — скачайте через View raw / Download raw file и распакуйте.
- [SHA-256 архива](DepotFlow-engineering-project.zip.sha256).
- [Инструкция запуска](engineering-project/README.md).
- [Атлас HTML](engineering-project/atlas/index.html) и [прототип HTML](engineering-project/design/prototype.html). GitHub показывает исходник HTML; интерактивный просмотр выполняется локально после скачивания.

Для проверенного локального просмотра из папки engineering-project:

```sh
python -m http.server 8765 --bind 127.0.0.1
```

Откройте http://127.0.0.1:8765/atlas/index.html или http://127.0.0.1:8765/design/prototype.html. Ctrl+C останавливает сервер. Node/npm, Figma и backend для просмотра не нужны. Прямое открытие HTML предусмотрено, но file:// не проверено браузером инструмента; подробности в QA-отчёте.

## Навигация для технического ревью

1. [Исходный промпт](engineering-project/research/original-brief.txt), [исследование и выбор продукта](engineering-project/research/market-study.md).
2. [PRD](engineering-project/product/PRD.md), [бизнес-процессы](engineering-project/product/business-processes.md), [user stories](engineering-project/product/stories/).
3. [Архитектура](engineering-project/architecture/), [контракты](engineering-project/contracts/), [диаграммы SVG и editable JSON](engineering-project/architecture/diagrams/).
4. [Все 18 заданий](engineering-project/assignments/), начиная с [M01](engineering-project/assignments/M01.md).
5. [Дизайн и исходники прототипа](engineering-project/design/), [исходники атласа](engineering-project/atlas/), [печатный handbook](engineering-project/exports/handbook.html).
6. [Матрица покрытия](engineering-project/reviews/requirements-coverage.md), [инвентаризация файлов](engineering-project/PROJECT_INDEX.md), [реальные проверки и ограничения](engineering-project/reviews/pack-quality.md), [raw evidence](engineering-project/reviews/evidence/).

Проверьте независимые границы сервисов и данных, конкурентное бронирование, идемпотентность платежей, физическую выдачу и возврат, карантин повреждённого оборудования с будущими бронями, учебную глубину заданий и согласованность контрактов. Критерии нагрузок, отказов и deployment относятся к будущей реализации; результаты таких испытаний backend не заявлены.

## Редактирование и воспроизведение QA

Все исходники и генераторы в [tools](engineering-project/tools/). Инструкция формальной валидации контрактов находится в README комплекта. node_modules и кэши исключены; package-lock сохранён. ZIP содержит тот же самостоятельный комплект engineering-project, без вспомогательного корневого README репозитория.
