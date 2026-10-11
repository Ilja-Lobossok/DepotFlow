"""One-time source refinement of prototype interactions (no business implementation)."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'design/prototype.js'
s=p.read_text(encoding='utf-8')
if 'let selection=' in s:
    print('Already refined; no changes')
    raise SystemExit(0)
s=s.replace("let bookingStatus='PENDING',jobStatus='READY',pageNo=1,filter='all';", "let bookingStatus='PENDING',jobStatus='READY',pageNo=1,filter='all';\nlet selection={name:'Cordless drill',daily:2500,deposit:10000,qty:1,days:2,start:'2026-11-02T08:00',end:'2026-11-04T08:00'}; const euros=n=>'€'+(n/100).toFixed(2); const rental=()=>selection.daily*selection.days*selection.qty, deposit=()=>selection.deposit*selection.qty, auth=()=>rental()+deposit();")
start=s.index('function summary()');end=s.index('function timeline()',start)
s=s[:start]+'''function summary(){return `<section class="panel summary"><span class="eyebrow">Неизменяемая котировка / DEMO</span><h2>${escapeHtml(selection.name)}</h2><p>Tallinn · UTC ${escapeHtml(selection.start)} → ${escapeHtml(selection.end)}<br>${selection.qty} экземпляр(а) · ${selection.days} × 24h</p><div class="row"><span>Аренда</span><strong>${euros(rental())}</strong></div><div class="row"><span>Возвратный депозит</span><strong>${euros(deposit())}</strong></div><div class="row"><span>Авторизация</span><strong>${euros(auth())}</strong></div><small>Средства списываются после возврата. В этой демонстрации реальных платежей нет.</small></section>`}
'''+s[end:]
start=s.index('function timeline()');end=s.index('function pageContent',start)
s=s[:start]+'''function timeline(){const cancelled=['CANCELLING','CANCELLED'].includes(bookingStatus);return `<ol class="timeline"><li>Котировка сохранена<small>Demo price snapshot ${euros(rental())} + депозит ${euros(deposit())}</small></li><li>Запрос Inventory записан<small>Временный hold / deadline10min</small></li><li class="${bookingStatus==='PENDING'?'pending':''}">${cancelled?'Запрошена компенсация / release + void':bookingStatus==='PENDING'?'Авторизация PSP ожидается':'Авторизация PSP получена'}<small>Stable provider key; unknown outcome never treated as decline</small></li><li class="${['PENDING','CANCELLING'].includes(bookingStatus)?'pending':''}">${bookingStatus==='CANCELLED'?'Компенсации подтверждены, allocation released':bookingStatus==='CANCELLING'?'CANCELLING: ожидаются доказательства':bookingStatus==='PENDING'?'Allocation ещё не подтверждена':'Allocation committed / физический workflow'}<small>Authoritative business state required in implementation</small></li></ol>`}
'''+s[end:]
s=s.replace('value="2026-11-02T08:00" required aria-describedby="form-error"','value="${selection.start}" required aria-describedby="form-error"').replace('value="2026-11-04T08:00" required aria-describedby="form-error"','value="${selection.end}" required aria-describedby="form-error"')
s=s.replace('value="1" min="1" max="5"','value="${selection.qty}" min="1" max="5"')
s=s.replace('<strong>€25.00</strong>','<strong>${euros(selection.daily)}</strong>').replace('<strong>48h → 2 дня</strong>','<strong>${selection.days} × 24h (rounded up)</strong>')
s=s.replace('Начать резерв · €150 авторизация','Начать резерв · ${euros(auth())} авторизация')
s=s.replace("if(pageNo===2)found=found.slice(-1);", "found=found.slice((pageNo-1)*2,pageNo*2);")
s=s.replace("${btn('Выбрать период','availability')}", "<a class=\"button primary\" data-model=\"${name}\" href=\"#availability\">Выбрать период</a>")
s=s.replace("location.hash='quote'});", "selection={...selection,start:document.querySelector('#start').value,end:document.querySelector('#end').value,qty,days:Math.ceil((b-a)/86400000)};location.hash='quote'});")
s=s.replace("filter=e.target.value;document.querySelector", "filter=e.target.value;pageNo=1;document.querySelector")
# Delegated model selection handles cards re-rendered by filter/search.
s += '''\nroot.addEventListener('click',e=>{const a=e.target.closest('[data-model]');if(a){const n=a.dataset.model;selection={...selection,name:n,daily:n==='Portable generator'?6000:n==='Impact driver'?2000:2500,deposit:n==='Portable generator'?20000:10000};}});\n'''
p.write_text(s,encoding='utf-8')
print('Prototype selection, pricing summary, pagination and cancellation timeline refined')
