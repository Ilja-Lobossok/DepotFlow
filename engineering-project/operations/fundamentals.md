# Foundations before commands

HTTP request/response: успешный transport response не доказывает завершение async процесса;202 означает durable acceptance,200/201 должны соответствовать обещанному ресурсу. DNS переводит имя в адрес, TCP устанавливает соединение, TLS проверяет шифрование/идентичность, HTTP описывает прикладной обмен. Port — адрес процесса, configured port не доказывает listening socket. Timeout говорит об отсутствии ответа, не об отсутствии выполненного эффекта.

Container изолирует процесс filesystem/network/cgroups, image immutable template, volume хранит данные отдельно от контейнера. Compose описывает локальные зависимости, Kubernetes поддерживает desired state/rollout, но не делает SQL данные автоматически HA. Linux signal SIGTERM просит graceful shutdown; SIGKILL не позволяет дописать транзакцию/ACK. Readiness решает получение трафика, liveness — жив процесс, startup даёт время инициализации.

SQL transaction атомарна внутри одного owner; MVCC позволяет concurrent reads, row lock защищает выбранные строки, isolation level влияет на аномалии. Exclusion constraint ограничивает пересечение двух rows. Index ускоряет конкретный доступ, но увеличивает write cost; EXPLAIN ANALYZE реально выполняет запрос, поэтому эксперимент с writes только lab/rollback. Миграция меняет schema, seed создаёт test data; это разные обязанности.

Redis in-memory key/value хранит cache/throttle; TTL ограничивает stale lifetime, eviction может удалить раньше. Cache не источник правды. Broker переносит сообщение, publisher confirm доказывает приём broker, ACK — признание consumer; ни одно само по себе не financial correctness. Outbox связывает domain write и будущую публикацию, inbox связывает dedupe и consumer effect. Saga — последовательность локальных транзакций с компенсацией; void не тот же DB rollback, физическая выдача может быть необратима.

Idempotency повторяет логический результат для одной operation identity. UUID нового HTTP request не равен business operation key. Retry/jitter ограничивают повтор и синхронизацию клиентов; DLQ хранит нерешённые сообщения, не удаляет проблему. Eventual consistency означает видимый lag projection; UX обязан показывать pending/stale, а correctness проверяется authoritative owner.

OAuth2 регулирует выдачу access, OIDC добавляет identity, JWT — signed token, RBAC — role permissions; проверка роли не заменяет ownership/depot. Trace объясняет одну causal цепочку, metrics показывают агрегаты, logs — события; correlation связывает async процесс. SLO — выбранная цель по определённому SLI/denominator/window; lab target не production SLA.

Git version-controls source, image digest identifies built artifact. CI автоматизирует проверки, CD доставляет проверенный artifact; rollback image не отменяет destructive schema change. OpenTofu state связывает configuration с resources, plan — предполагаемые изменения, apply — реальные; Ansible converges existing hosts. Ни apply, ни изменение личных VM не выполняются автором этого пакета.

Перед любой новой Linux/DevOps командой студент должен указать: где выполнять (Windows editor/Linux lab/repo root/namespace), цель, каждый аргумент, ожидаемый результат, команду доказательства и безопасное восстановление. После ответа тьютор объясняет пробелы; не даёт готовую бизнес-реализацию. Справочные команды будущих tests явно labeled в reviews/test-strategy.md.
