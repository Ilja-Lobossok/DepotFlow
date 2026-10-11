# DepotFlow — самостоятельный Microservices Engineering Capstone

Начните с **[локального атласа](atlas/index.html)**: открыть файл двойным щелчком в Chrome/Edge. Интернет, Figma, npm и backend для просмотра не нужны. [Интерактивный прототип продукта](design/prototype.html) также открывается файлом. Если браузер запрещает localStorage у file://, используйте экспорт JSON или локальный просмотр: `python -m http.server 8765 --bind 127.0.0.1` из engineering-project, затем http://127.0.0.1:8765/atlas/index.html; Ctrl+C останавливает сервер. Python запускается в этой папке, -m выбирает встроенный модуль, порт8765 локальный, --bind не выставляет сервер в сеть. Проверьте загрузку страницы, а не только сообщение о старте.

## Что вы получили

DepotFlow — вымышленная коммерчески реалистичная B2B платформа аренды оборудования:7бизнес-сервисов, конкурентные временные резервы, payment saga, физическая выдача, возврат/ремонт, settlement/refund. Target настоящие микросервисы, отдельные владельцы данных, независимые build/test/deploy. Это проектное задание, контракты и инструменты просмотра; готового backend бизнес-продукта здесь нет.

18последовательных milestones;20user stories;12NFR;10ADRs;15дорожных карт;43отрисованныеSVG схемы;22экрана responsive prototype;7OpenAPI+7AsyncAPI;23JSON event schemas ивалидируемые fixtures. Критерии относятся к будущей самостоятельно реализованной системе. Прогресс атласа — личная отметка, не свидетельство выполнения backend.

## Как начать обучение

1. Прочитать research/market-study.md, product/PRD.md и business-processes.md.
2. Изучить System context/Container diagram и passport Inventory/Booking/Billing в атласе.
3. Открыть assignments/M01.md; объяснить новые понятия, создать изолированное окружение самостоятельно.
4. Практика → результаты и evidence → ревью → разбор ошибок → подтверждение навыка. Не переходить дальше по галочке без прохождения критериев.

Этапы не привязаны к сроку. Пороги нагрузок/RTO — design targets лаборатории, не гарантии коммерческой системы. Cloud optional: вся обязательная программа локальна; live AWS требует отдельного разрешения на расходы и не выполнена в этом комплекте. Версии implementation pin самостоятельно в M01 после compatibility check.

## Источники и изменение

Исследовано11.10.2026; доступность вакансий не гарантируется. Статусы expired/unconfirmed отделены в research/sources.json, статистика рынка не придумана. Исходный brief сохранён research/original-brief.txt. Основной текст преимущественно русский, технические термины и часть проверок английские.

Редактировать tools/build_content.py (product/tasks/docs), build_contracts.py (API/events), build_visuals.py (diagram semantics/layout); atlas/* и design/* редактируются напрямую. `python tools/build_pack.py` регенерирует материалы, не business code; `python tools/verify_pack.py` проверяет пакет стандартной библиотекой. Для повторной **формальной** проверки контрактов: из tools/validators выполнить `npm ci --ignore-scripts`, затем из project root `node tools/validate-contracts.cjs`; нужны интернет и npm только для QA, не чтения.

Состояние реальных проверок: reviews/pack-quality.md и reviews/evidence/*.json. [Индекс](PROJECT_INDEX.md), [матрица покрытия](reviews/requirements-coverage.md), [печатный handbook](exports/handbook.html). Единый ZIP находится рядом с engineering-project; архив не включает node_modules и не требует установки пакетов для просмотра.
