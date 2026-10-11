"""Regenerate documentation + SVG + offline atlas content; does not implement business services."""
from build_visuals import *
import supplement_content
from datetime import datetime, timezone
write('product/business-processes.md',DOCS['product/business-processes.md']+'\n\n## Membership safety\n\nTenancy rejects revocation/demotion of last active org_admin with409 last_admin; locks organization and memberships atomically to prevent concurrent removal of two last admins. Invite/role update cannot assign operator without a valid same-org depot. Audit actor/reason/version persists with membership change. Initial org and first admin are synthetic bootstrap fixtures, not open public sign-up in core.')

write('README.md', '''# DepotFlow — самостоятельный Microservices Engineering Capstone

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
''')
write('operations/fundamentals.md', '''# Foundations before commands

HTTP request/response: успешный transport response не доказывает завершение async процесса;202 означает durable acceptance,200/201 должны соответствовать обещанному ресурсу. DNS переводит имя в адрес, TCP устанавливает соединение, TLS проверяет шифрование/идентичность, HTTP описывает прикладной обмен. Port — адрес процесса, configured port не доказывает listening socket. Timeout говорит об отсутствии ответа, не об отсутствии выполненного эффекта.

Container изолирует процесс filesystem/network/cgroups, image immutable template, volume хранит данные отдельно от контейнера. Compose описывает локальные зависимости, Kubernetes поддерживает desired state/rollout, но не делает SQL данные автоматически HA. Linux signal SIGTERM просит graceful shutdown; SIGKILL не позволяет дописать транзакцию/ACK. Readiness решает получение трафика, liveness — жив процесс, startup даёт время инициализации.

SQL transaction атомарна внутри одного owner; MVCC позволяет concurrent reads, row lock защищает выбранные строки, isolation level влияет на аномалии. Exclusion constraint ограничивает пересечение двух rows. Index ускоряет конкретный доступ, но увеличивает write cost; EXPLAIN ANALYZE реально выполняет запрос, поэтому эксперимент с writes только lab/rollback. Миграция меняет schema, seed создаёт test data; это разные обязанности.

Redis in-memory key/value хранит cache/throttle; TTL ограничивает stale lifetime, eviction может удалить раньше. Cache не источник правды. Broker переносит сообщение, publisher confirm доказывает приём broker, ACK — признание consumer; ни одно само по себе не financial correctness. Outbox связывает domain write и будущую публикацию, inbox связывает dedupe и consumer effect. Saga — последовательность локальных транзакций с компенсацией; void не тот же DB rollback, физическая выдача может быть необратима.

Idempotency повторяет логический результат для одной operation identity. UUID нового HTTP request не равен business operation key. Retry/jitter ограничивают повтор и синхронизацию клиентов; DLQ хранит нерешённые сообщения, не удаляет проблему. Eventual consistency означает видимый lag projection; UX обязан показывать pending/stale, а correctness проверяется authoritative owner.

OAuth2 регулирует выдачу access, OIDC добавляет identity, JWT — signed token, RBAC — role permissions; проверка роли не заменяет ownership/depot. Trace объясняет одну causal цепочку, metrics показывают агрегаты, logs — события; correlation связывает async процесс. SLO — выбранная цель по определённому SLI/denominator/window; lab target не production SLA.

Git version-controls source, image digest identifies built artifact. CI автоматизирует проверки, CD доставляет проверенный artifact; rollback image не отменяет destructive schema change. OpenTofu state связывает configuration с resources, plan — предполагаемые изменения, apply — реальные; Ansible converges existing hosts. Ни apply, ни изменение личных VM не выполняются автором этого пакета.

Перед любой новой Linux/DevOps командой студент должен указать: где выполнять (Windows editor/Linux lab/repo root/namespace), цель, каждый аргумент, ожидаемый результат, команду доказательства и безопасное восстановление. После ответа тьютор объясняет пробелы; не даёт готовую бизнес-реализацию. Справочные команды будущих tests явно labeled в reviews/test-strategy.md.
''')

# Requirement-to-artifact coverage including each original brief section.
coverage=[]
for s in stories:
    coverage.append(dict(id=s['id'],spec=f"product/stories/{s['id']}.md",assignment=f"assignments/{s['milestone']}.md",acceptance=s['acceptance'],screens=s['screens'],status='specified; implementation unstarted',evidence='student evidence/'+s['milestone']))
for i,t,a,m in NFR:coverage.append(dict(id=i,spec='requirements/nonfunctional.md',assignment='assignments/'+m+'.md',acceptance=a,screens=[],status='specified; implementation unstarted',evidence='student evidence/'+m))
for j in range(1,12):coverage.append(dict(id=f'A{j:02}',spec='reviews/engineering-audit.md',assignment='assignments/M18.md',acceptance='Audit gate row A'+str(j).zfill(2),screens=[],status='specified; implementation unstarted',evidence='student evidence/M18'))
dump('reviews/coverage.json',coverage)
briefmap=[
 ('B01','Роль / самостоятельность','README.md; assignments/M01.md','Business implementation intentionally student-owned'),
 ('B02','Исследование / выбор','research/market-study.md; research/sources.json','Primary sources checked; expired jobs explicit'),
 ('B03','Реальные микросервисы','architecture/system-design.md; architecture/services.json','7business owners, private DB, independent deployment criteria'),
 ('B04','PRD / бизнес-логика / stories','product/PRD.md; product/business-processes.md; product/stories/F01.md','20full stories, precise states and acceptance'),
 ('B05','System Design / contracts / distributed','architecture/diagrams/index.json; contracts/README.md','43rendered SVG, 7OpenAPI+7AsyncAPI, fault mechanisms'),
 ('B06','Стек и глубина','architecture/technology-decisions.md; operations/fundamentals.md','Problem/alternative/limit/practice/proof for17technology groups'),
 ('B07','Учебные задания','assignments/milestones.json; reviews/reviewer-guide.md','18docs with all required sections'),
 ('B08','UI/UX','design/prototype.html; design/design-spec.md; design/screens.json','22responsive screens; role/journey/state controls'),
 ('B09','Интерактивный атлас / roadmap','atlas/index.html; roadmaps/tracks.json','12sections,15visual dependency tracks, local progress/export'),
 ('B10','Engineering process','operations/engineering-process.md; operations/templates/pull_request.md','Templates, ADR, migration, release, rollback, runbooks'),
 ('B11','Финальный результат / audit','reviews/engineering-audit.md; requirements/nonfunctional.md','11audit gates and quantitative lab thresholds'),
 ('B12','Файлы / архив / исходники','PROJECT_INDEX.md; tools/build_pack.py; exports/handbook.html','Local first; ZIP excludes validator dependencies'),
 ('B13','Quality / coverage','reviews/pack-quality.md; reviews/coverage.json','Pack QA separate from future runtime evidence'),
 ('B14','Фазы A–F','reviews/phase-register.md','Research/design/visual/assignments/packaging/audit recorded'),
 ('B15','Учебный подход','operations/fundamentals.md; operations/engineering-process.md','Explain→independent practice→review→errors→confirmation')
]
dump('reviews/brief-coverage.json',[dict(id=i,section=t,files=f.split('; '),status=s) for i,t,f,s in briefmap])
write('reviews/requirements-coverage.md','# Матрица покрытия\n\nCoverage означает наличие спецификации и критериев, а не реализованную бизнес-систему. Все F/N/A реализации UNSTARTED.\n\n| ID | Specification | Assignment | Acceptance | Implementation |\n|---|---|---|---|---|\n'+'\n'.join(f"|{c['id']}|[{c['spec']}](../{c['spec']})|[{c['assignment']}](../{c['assignment']})|{c['acceptance'].replace('|','/')}|unstarted|" for c in coverage)+'\n\n## Original brief coverage\n\n| ID | Requirement | Artifacts | Readiness |\n|---|---|---|---|\n'+'\n'.join(f'|{i}|{t}|'+', '.join(f'[{p}](../{p})' for p in f.split('; '))+f'|{s}|' for i,t,f,s in briefmap))
write('reviews/phase-register.md', '''# Phase register / scope accounting

| Phase | Output | Status |
|---|---|---|
| A Research / selection |market study with dated primary-source URLs, four scored domains|created / sources checked11Oct2026|
| B Product / architecture |PRD,10processes,20stories,12NFR,7passports,models,contracts,10ADRs|created / formal schema validation separately recorded|
| C UI / visuals |22screens interactive prototype,design system,43SVG+JSON layouts|created / browser QA evidence records checked samples|
| D Assignments |18complete milestones,15roadmaps,reviewer/audit/test strategy|created / structural and referential checks|
| E Atlas / packaging |12sections offline reader,local progress,source JSON/JS,print handbook,ZIP|created / local and browser checks|
| F Quality audit |coverage matrices,file inventory,validator reports,UI evidence|completed for pack; runtime system audit deliberately future M18|

No claims that future implementation functions, Kubernetes deployed, load thresholds achieved, payment reconciles live, or cloud resources provisioned. Those are student acceptance tasks, not packaging results. Figma, cloud hosting and live AWS not required and not used. Interactive mock can demonstrate behavior but is not production security or persistence.
''')
dump('assignments/backlog.json',[dict(id=f'{m[0]}-T{j:02}',milestone=m[0],epic=('E01' if int(m[0][1:])<=3 else 'E02' if int(m[0][1:])<=5 else 'E03' if int(m[0][1:])<=8 else 'E04' if int(m[0][1:])<=10 else 'E05' if int(m[0][1:])<=12 else 'E06' if int(m[0][1:])<=17 else 'E07'),title=t,details=d,status='unstarted') for m in MILESTONES for j,t,d in [(1,'Design / contract review',m[4]),(2,'Independent implementation',m[5]),(3,'Failure and acceptance evidence',m[6]+'; '+m[8]),(4,'Review / skill confirmation',m[9]+'; '+m[10])]])

# QA report incorporates only evidence actually executed; skipped work stays explicit.
report_path=ROOT/'reviews/evidence/contract-validation.json'
contract=json.loads(report_path.read_text(encoding='utf-8')) if report_path.exists() else {}
browser_path=ROOT/'reviews/evidence/browser-qa.json'
browser=json.loads(browser_path.read_text(encoding='utf-8')) if browser_path.exists() else {}
write('reviews/pack-quality.md',f'''# Pack quality report

Артефакты созданы локально; future business runtime not implemented. Проверки и ограничения ниже относятся **только к комплекту задания**.

## Executed contract checks
@apidevtools/swagger-parser: {len(contract.get('openapi',[]))}/7 OpenAPI. @asyncapi/parser: {len(contract.get('asyncapi',[]))}/7 AsyncAPI. Ajv2020+formats: {len(contract.get('eventSchemas',[]))}/23 event schemas, valid generated examples + negative missing event_id. Formal errors: {len(contract.get('errors',[])) if contract else 'not run'}. Raw report: reviews/evidence/contract-validation.json. Parser semantic warnings retained; inspect rather than hide them. Syntax validation does not prove business correctness.

## Executed browser checks
Browser evidence: {len(browser.get('checks',[]))}checks recorded. Raw browser-qa.json and JPEG/screenshots in reviews/evidence. Navigation, pending/confirmed simulation, role/warehouse paths, state display, filter/search, progress reload, zoom and responsive checks are pack tests, not backend E2E. Exact tested widths and omissions in raw report. Source `node --check` for atlas/app.js and design/prototype.js executed. Document links/refs/registries, XML SVG and dependency DAG checked by tools/verify_pack.py; raw pack-validation.json generated after packaging.

## Limitations / unfinished verification
Future7service runtime, Docker/Kubernetes deployment, load/security/resilience/restore and independent-release audits: **UNIMPLEMENTED BY DESIGN**, student M01–M18. Prototype is visual reference, not auth/payment/business implementation. Full screen-reader audit and visual inspection of every SVG at every zoom not performed; browser QA samples plus source checks, no accessibility certification. Live-cloud IAM/cost/deployment not verified, mandatory practice local. Search evidence freshness is11Oct2026; missing or expired jobs labeled. Source contracts/fixtures verified schema-wise, not through a running provider.

Browser QA executed over loopback HTTP. Direct file:// navigation is blocked by in-app browser URL policy, so file-mode opening is **not browser-tested**. No workaround of that policy used; package source uses only local assets without fetch/CDN so direct open is the intended external-browser usage, while the tested localhost path is documented in README.

The offline HTMLs and editable source suffice to start implementation. Local file storage may vary by browser, export progress supported. ZIP contains versioned sources, contracts and rendered assets; no CDN/node_modules requirement. README and index contain actual paths. Completion inventory in PROJECT_INDEX.md records material readiness, not student pass status.
''')

def simple_md(src,source_path='README.md'):
    # Static HTML export with readable tables and working source/external links.
    out=[];code=False;lines=src.splitlines();i=0
    def fmt(s):
        v=html.escape(s)
        v=re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',v)
        v=re.sub(r'`([^`]+)`',r'<code>\1</code>',v)
        def mdlink(m):
            label,url=m[1],html.unescape(m[2])
            if not url.startswith(('https://','http://','#')):
                target=(ROOT/source_path).parent/url
                try:url='../'+target.resolve().relative_to(ROOT).as_posix()
                except ValueError:url='#'
            return '<a href="'+html.escape(url,quote=True)+'">'+label+'</a>'
        v=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',mdlink,v)
        return v
    while i<len(lines):
        line=lines[i];i+=1
        if not code and line.startswith('|') and i<len(lines) and re.fullmatch(r'\|[- :|]+\|',lines[i].strip()):
            rows=[line];i+=1
            while i<len(lines) and lines[i].startswith('|'):rows.append(lines[i]);i+=1
            table='<table><thead><tr>'+''.join('<th>'+fmt(x.strip())+'</th>' for x in rows[0].strip().strip('|').split('|'))+'</tr></thead><tbody>'
            table+=''.join('<tr>'+''.join('<td>'+fmt(x.strip())+'</td>' for x in row.strip().strip('|').split('|'))+'</tr>' for row in rows[1:])+'</tbody></table>'
            out.append(table);continue
        if line.startswith('```'):code=not code;out.append('<pre>' if code else '</pre>');continue
        if code:out.append(html.escape(line));continue
        m=re.match(r'^(#{1,6}) (.+)',line)
        if m:out.append(f'<h{len(m[1])}>{fmt(m[2])}</h{len(m[1])}>')
        elif line.strip():out.append('<p>'+fmt(line)+'</p>')
    return '\n'.join(out)

# Reproducible offline print book. Source documents remain the canonical editable version.
paths=list(DOCS)
bookcss='body{font:15px/1.65 Segoe UI,Arial,sans-serif;color:#152e3e;margin:auto;max-width:1000px;padding:36px}h1{font-size:28px}h2{font-size:21px}section{border-top:1px solid #ccd8df;margin-top:36px;padding-top:24px}nav a{display:block;padding:3px;color:#075d64}p,td,th{overflow-wrap:anywhere}table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:10px;border:1px solid #ccd8df;text-align:left;vertical-align:top}th{background:#edf3f5}tr{break-inside:avoid}pre{white-space:pre-wrap}img{width:100%;max-height:850px;object-fit:contain}@media print{nav,button{display:none}section{break-before:page;border:0}body{padding:0;font-size:10pt}a{color:black}}'
book='<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>DepotFlow Print Handbook</title><style>'+bookcss+'</style></head><body><h1>DepotFlow Engineering Handbook</h1><p>Offline print/export reference · all source Markdown retained · no business implementation</p><button onclick="window.print()">Печать / сохранить PDF средствами браузера</button><nav>'+'\n'.join(f'<a href="#d{i}">{html.escape(p)}</a>' for i,p in enumerate(paths))+'</nav>'
book+='\n'.join(f'<section id="d{i}"><small>{html.escape(p)}</small>{simple_md(DOCS[p],p)}</section>' for i,p in enumerate(paths))
book+='<section><h1>Rendered diagram plates</h1>'+''.join(f'<h2>{html.escape(d["title"])}</h2><img src="../{d["path"]}" alt="{html.escape(d["title"])}">' for d in DIAGRAMS)+'</section></body></html>'
write('exports/handbook.html',book)
files=[p for p in ROOT.rglob('*') if p.is_file() and 'node_modules' not in p.parts and '__pycache__' not in p.parts and p.name!='PROJECT_INDEX.md']
write('PROJECT_INDEX.md','# Project index / material readiness\n\nMain entry: atlas/index.html. Source inputs tools/build_*.py and atlas/design JS/CSS/HTML. Ready = file created; actual QA limits in reviews/pack-quality.md; business implementation unstarted.\n\n| File | Material status |\n|---|---|\n'+'\n'.join(f'|[{p.relative_to(ROOT).as_posix()}]({p.relative_to(ROOT).as_posix()})|created|' for p in sorted(files)))
finish_registry()
print('Pack generated:',len(DOCS),'documents;',len(DIAGRAMS),'diagrams;',len(SCREENS),'screens')
