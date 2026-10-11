from build_contracts import *
from xml.sax.saxutils import escape
DIAGRAMS=[]
def svg_text(x,y,label,size=14,color='#dce8f4',anchor='start'):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" text-anchor="{anchor}" font-family="Segoe UI,Arial,sans-serif">{escape(str(label))}</text>'
def head(w,h,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#68cbd4"/></marker></defs><rect width="{w}" height="{h}" fill="#101d2c"/>'+svg_text(32,38,title,22)+svg_text(32,64,'DepotFlow • Design specification • стрелки = разрешённые потоки, не измеренная нагрузка',12,'#92a9bd')
def save_diagram(slug,title,kind,source,svg,doc='architecture/system-design.md'):
    write(f'architecture/diagrams/{slug}.json',json.dumps(source,ensure_ascii=False,indent=2))
    write(f'architecture/diagrams/{slug}.svg',svg)
    DIAGRAMS.append(dict(id=slug,title=title,kind=kind,source=f'architecture/diagrams/{slug}.json',path=f'architecture/diagrams/{slug}.svg',doc=doc,svg=svg))
def graph(slug,title,kind,nodes,edges,doc='architecture/system-design.md',width=1240,height=640,groups=None):
    # node: id,label,description,x,y,width(optional),height(optional),service(optional)
    nd={n[0]:n for n in nodes}; out=head(width,height,title)
    for label,x,y,w,h in groups or []:
        out+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#182b3d" stroke="#455e73" stroke-dasharray="7 5"/>'+svg_text(x+16,y+25,label,13,'#9fb3c5')
    for a,b,label in edges:
        n,m=nd[a],nd[b];nw=n[5] if len(n)>5 else 230;nh=n[6] if len(n)>6 else 86;mw=m[5] if len(m)>5 else 230;mh=m[6] if len(m)>6 else 86
        x1,y1=n[3]+nw/2,n[4]+nh/2;x2,y2=m[3]+mw/2,m[4]+mh/2
        if abs(x2-x1)>abs(y2-y1):x1+=nw/2*(1 if x2>x1 else-1);x2-=mw/2*(1 if x2>x1 else-1)
        else:y1+=nh/2*(1 if y2>y1 else-1);y2-=mh/2*(1 if y2>y1 else-1)
        out+=f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#68cbd4" stroke-width="2" marker-end="url(#arr)"/>'
        lx,ly=(x1+x2)/2,(y1+y2)/2
        out+=f'<rect x="{lx-len(label)*3.4}" y="{ly-14}" width="{len(label)*6.8+12}" height="22" rx="4" fill="#101d2c"/>'+svg_text(lx+5,ly+1,label,11,'#dce8f4','middle')
    for n in nodes:
        nid,label,desc,x,y=n[:5];w=n[5] if len(n)>5 else 230;h=n[6] if len(n)>6 else 86
        service=n[7] if len(n)>7 else (nid if nid in [s['id'] for s in SERVICES] else '')
        out+=f'<g data-service="{service}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#20364a" stroke="{ "#efab58" if service else "#527189"}" stroke-width="1.5"/>'+svg_text(x+16,y+29,label,16)
        for j,line in enumerate(desc.split('|')): out+=svg_text(x+16,y+50+j*17,line,11,'#a8bdce')
        out+='</g>'
    out+='</svg>'
    save_diagram(slug,title,kind,dict(title=title,kind=kind,width=width,height=height,nodes=nodes,edges=edges,groups=groups or []),out,doc)

graph('context','System context','Context',[
 ('client','Корпоративный клиент','Поиск • аренда • отмена',35,110),('operator','Сотрудник склада','Выдача • возврат • ремонт',35,280),('admin','Admin / Finance','Роли • тариф • refund',35,450),('system','DepotFlow','B2B rental platform|7 business owners',485,260,270,110),('idp','Keycloak','Authentication / OIDC',920,120),('psp','Sandbox PSP','Authorization • query • capture',920,290),('mail','Mail sink','Synthetic messages only',920,460)], [('client','system','HTTPS'),('operator','system','HTTPS'),('admin','system','HTTPS'),('system','idp','OIDC/JWKS'),('system','psp','Billing only'),('system','mail','Notification only')])
nodes=[('web','React / TypeScript','Browser • no private DB access',40,110),('gateway','Gateway / Nginx','Routes • TLS • throttle',40,290),('idp','Keycloak','Identity infrastructure',40,470)]
for i,s in enumerate(SERVICES):
    x=370+(i%4)*280;y=110+(i//4)*290
    nodes += [(s['id'],s['name'],s['purpose'][:24]+'|Own HTTP + contracts',x,y,240,86),(s['id']+'_db',s['name']+' DB','Private PostgreSQL database',x,y+120,240,70)]
nodes += [('broker','RabbitMQ','Commands + facts • durable',1210,465,240,86)]
edges=[('web','gateway','HTTPS'),('web','idp','PKCE'),('gateway','booking','HTTP'),('gateway','catalog','HTTP')]+[(s['id'],s['id']+'_db','owner only') for s in SERVICES]+[(s['id'],'broker','AMQP') for s in SERVICES if s['consumes'] or s['publishes']]
graph('containers','Container diagram — 7 independent business services','Containers',nodes,edges,width=1520,height=680)
for owner in ['inventory','booking','billing']:
    graph('component-'+owner,'Component: '+owner.title(),'Components',[
     ('http','HTTP / auth adapter','JWT • tenant • validation',45,160),('domain','Domain application','Transitions • version • invariants',390,160),('repo','Owned repository','DB transaction • locks',740,160),('inbox','AMQP consumer','Schema • inbox • ACK after commit',45,390),('outbox','Outbox publisher','mandatory + confirm → published',390,390),('adapter','Scheduler / provider adapter','Lease/reconcile' if owner!='billing' else 'PSP stable key outside DB lock',740,390)], [('http','domain','command'),('inbox','domain','effect'),('domain','repo','atomic write'),('repo','outbox','committed outbox'),('adapter','domain','resume/query'),('outbox','inbox','via RabbitMQ')],doc=f'architecture/services/{owner}.md',width=1060,height=560)

def sequence(slug,title,actors,msgs):
    w=max(1000,len(actors)*200+60);h=150+len(msgs)*62;out=head(w,h,title);pos={a:80+i*(w-160)/(len(actors)-1) for i,a in enumerate(actors)}
    for a,x in pos.items():out+=f'<rect x="{x-72}" y="84" width="144" height="40" rx="6" fill="#20364a"/>'+svg_text(x,110,a,13,anchor='middle')+f'<path d="M{x} 124 V{h-20}" stroke="#527189" stroke-dasharray="5 4"/>'
    for i,(a,b,label,typ) in enumerate(msgs):
        y=160+i*62;x1,x2=pos[a],pos[b]
        if a==b:out+=f'<path d="M{x1} {y} h60 v25 h-60" fill="none" stroke="#efab58" marker-end="url(#arr)"/>';tx=x1+70
        else:out+=f'<path d="M{x1} {y} H{x2}" stroke="{ "#efab58" if typ=="sync" else "#68cbd4"}" stroke-width="2" stroke-dasharray="{ "0" if typ=="sync" else "6 4"}" marker-end="url(#arr)"/>';tx=(x1+x2)/2
        out+=svg_text(tx,y-9,str(i+1)+'. '+label,11,anchor='middle' if a!=b else 'start')
    save_diagram(slug,title,'Sequence',dict(actors=actors,messages=msgs,width=w,height=h),out+'</svg>','product/business-processes.md')
sequence('sequence-checkout','Sequence — confirmation saga',['Client','Catalog','Booking','Inventory','Billing'],[
 ('Client','Catalog','POST quote → immutable snapshot','sync'),('Client','Booking','POST booking + key →202','sync'),('Booking','Inventory','reserve-requested via outbox','async'),('Inventory','Booking','hold.created (expires_at)','async'),('Booking','Billing','authorize-requested (stable key)','async'),('Billing','Booking','payment.authorized','async'),('Booking','Inventory','commit-requested','async'),('Inventory','Booking','allocation.committed','async'),('Booking','Client','GET status CONFIRMED','sync')])
sequence('sequence-cancel','Sequence — late authorization after expiry',['Client','Booking','Inventory','Billing'],[
 ('Client','Booking','cancel + version','sync'),('Booking','Inventory','release-requested / tombstone','async'),('Inventory','Booking','allocation.released','async'),('Billing','Booking','late payment.authorized','async'),('Booking','Billing','void-requested (same intent)','async'),('Billing','Booking','payment.voided full','async'),('Booking','Client','GET CANCELLED after evidence','sync')])
sequence('sequence-handover-return','Sequence — physical fence and settlement',['Operator','Fulfillment','Booking','Inventory','Billing'],[
 ('Operator','Fulfillment','handover + If-Match','sync'),('Fulfillment','Inventory','physical eligibility / allocation check','sync'),('Fulfillment','Booking','claim atomically vs cancel','sync'),('Booking','Fulfillment','claim_id; cancellation fenced','sync'),('Fulfillment','Booking','handed-over fact (also Inventory)','async'),('Operator','Fulfillment','return inspection','sync'),('Fulfillment','Inventory','returned fact / release or quarantine','async'),('Fulfillment','Booking','returned fact','async'),('Inventory','Booking','allocation.released','async'),('Booking','Billing','settle-requested','async'),('Billing','Booking','captured + void remainder','async')])
graph('event-flow','Event flow — durable business effect','Events',[
 ('tx','Producer owned DB','Business change + outbox|One transaction',35,150),('pub','Publisher worker','Persistent • mandatory • confirms',350,150),('broker','RabbitMQ','Durable exchange / queue',680,150),('consume','Consumer transaction','Inbox + business + new outbox',680,380),('ack','ACK after commit','Lost ACK → safe redelivery',350,380),('dlq','DLQ quarantine','Poison/5attempts → operator',35,380)], [('tx','pub','poll'),('pub','broker','confirm'),('broker','consume','deliver'),('consume','ack','commit then ACK'),('consume','dlq','retry budget'),('ack','broker','redelivery dedupe')])

for s in SERVICES:
    tables=list(s['tables'].items());cols=2;w=1320;h=130+((len(tables)+1)//2)*330;out=head(w,h,'ER — '+s['name']+' owned database')
    positions={}
    for i,(table,columns) in enumerate(tables):
        x=40+(i%2)*660;y=100+(i//2)*330;positions[table]=(x,y)
        out+=f'<rect x="{x}" y="{y}" width="580" height="290" rx="12" fill="#20364a" stroke="#efab58"/>'+svg_text(x+20,y+32,table,18)
        for j,col in enumerate(columns.split(', ')):out+=svg_text(x+20,y+60+j*17,('PK ' if col=='id' else '')+col,12,'#c3d4e2')
    # Only own-database logical associations.
    relations={
     'tenancy':[('organizations','memberships','1 : many org_id'),('organizations','audit_entries','1 : many org_id')],
     'catalog':[('models','rates','1 : many model_id'),('models','quotes','1 : many model_id')],
     'inventory':[('depots','assets','1 : many depot_id'),('assets','allocations','1 : many asset_id'),('holds','allocations','1 : many hold_id'),('assets','maintenance_jobs','1 : many asset_id')],
     'booking':[('bookings','sagas','1 : 1 booking_id'),('bookings','timeline_entries','1 : many booking_id')],
     'billing':[('payment_intents','payment_operations','1 : many intent_id'),('payment_intents','provider_events','1 : many intent_id'),('payment_intents','ledger_entries','1 : many intent_id')],
     'fulfillment':[('jobs','handover_records','1 : 0..1 job_id'),('jobs','return_reports','1 : 0..1 job_id')],
     'notification':[('notifications','deliveries','1 : many notification_id')]
    }[s['id']]
    for a,b,label in relations:
        x1,y1=positions[a];x2,y2=positions[b]
        # Place relation labels along reserved margins so table columns remain legible.
        if y1==y2:out+=f'<path d="M{x1+580},{y1+250} H{x2}" stroke="#68cbd4" marker-end="url(#arr)"/>'+svg_text((x1+x2+580)/2,y1+242,label,10,anchor='middle')
        else:out+=f'<path d="M{x1+540},{y1+290} V{y2-15} H{x2+540} V{y2}" fill="none" stroke="#68cbd4" marker-end="url(#arr)"/>'+svg_text(x2+300,y2-20,label,11)
    save_diagram('er-'+s['id'],'ER — '+s['name'],'ER',dict(owner=s['id'],tables=s['tables'],relations=relations,width=w,height=h),out+'</svg>',f"data/models/{s['id']}.md")
for env,desc in [('local','Compose • 1host • not HA'),('test','Ephemeral test environment • fixed fixture'),('production-like','kind/k3d • same physical host • not cloud HA')]:
    graph('deployment-'+env,'Deployment — '+env,'Deployment',[
     ('edge','Ingress / browser','TLS443 / local loopback',50,145),('services','7service images','Independent digests/migrations|'+desc,405,145,360,100),('storage','Owned DBs / volumes','7credentials; backup metadata',405,375,360,90),('broker','RabbitMQ / Redis','1node or3quorum lab',905,145,270,90),('obs','OTel/Grafana','Restricted operator network',905,375,270,90),('backup','Isolated backup target','Checksums / restore namespace',50,375)], [('edge','services','HTTP'),('services','storage','own SQL'),('services','broker','AMQP/cache'),('services','obs','telemetry'),('storage','backup','snapshot')],doc='operations/environments.md')
graph('network','Network — allowed direction and trust','Network',[
 ('browser','Browser','Public client',50,145),('edge','Gateway / IdP','HTTPS443 only public ingress',380,145),('apps','App namespace','7 scoped service identities',730,145,360,90),('db','Private Postgres','DB role owner-only5432',730,380,360,90),('amqp','Private RabbitMQ','AMQPS5671 per-service ACL',380,380,260,90),('telemetry','Operator telemetry','4317 + restricted dashboards',50,380,250,90)], [('browser','edge','HTTPS'),('edge','apps','forward JWT'),('apps','db','owned TLS'),('apps','amqp','ACL'),('apps','telemetry','OTLP')],doc='operations/network-security.md',groups=[('Untrusted',20,90,280,180),('Edge boundary',340,90,300,180),('Private network / deny by default',690,90,450,440)])
graph('ci-cd','CI/CD — service-scoped delivery DAG','CI/CD',[
 ('diff','Change discovery','Source + contracts + reverse deps',35,130),('test','Tests / contracts','Unit • integration • old reader',360,130),('image','Artifact','Image digest • SBOM • scan',685,130),('migrate','Migration gate','Expand • compatibility proof',35,375),('deploy','Deploy one service','Health + smoke +5min observe',360,375),('rollback','Rollback decision','Old image; schema remains expanded',685,375)], [('diff','test','affected set'),('test','image','checks pass'),('image','migrate','promote digest'),('migrate','deploy','job passes'),('deploy','rollback','failure gate'),('rollback','deploy','verify recovery')],doc='operations/release-rollback.md',width=1010,height=560)
graph('observability','Observability — correlate metrics, logs and traces','Observability',[
 ('apps','7services + adapters','HTTP / AMQP trace context',40,130,290,90),('collector','OTel collector','Batch • redact • bounded queue',415,130,310,90),('tempo','Tempo','Causal spans/exemplars',870,130,280,90),('prom','Prometheus','Histograms; low-cardinality labels',40,380,290,90),('loki','Loki','JSON logs; no JWT/email',415,380,310,90),('grafana','Grafana / alerts','SLO / queue age / saga pending',870,380,280,90)], [('apps','collector','OTLP'),('collector','tempo','traces'),('apps','prom','scrape'),('collector','loki','logs'),('prom','grafana','SLI'),('loki','grafana','trace_id'),('tempo','grafana','trace links')],doc='reviews/test-strategy.md')
graph('security','Security — identity is checked at every boundary','Security',[
 ('browser','Client PKCE','JWT in memory; not roles authority',35,135,285,90),('keycloak','Keycloak','Issuer / audience / expiry / JWKS',420,135,310,90),('service','Business service','Tenant + resource + role check',855,135,300,90),('tenancy','Tenancy authority','Mutation membership check; reads≤60s',420,390,310,90),('resources','DB / broker / PSP','Own role • scoped ACL • callback HMAC',855,390,300,90)], [('browser','keycloak','authenticate'),('browser','service','gateway JWT'),('service','keycloak','verify key'),('service','tenancy','authorize'),('service','resources','least privilege')],doc='operations/network-security.md')
graph('failure-recovery','Failure/recovery — ambiguous PSP authorization','Failure',[
 ('timeout','PSP response lost','Provider may already have charged',35,135,285,90),('unknown','Billing UNKNOWN','Persist operation / stable key',420,135,300,90),('lookup','Provider lookup','Same key; never new authorization',855,135,300,90),('active','Hold still active?','Inventory clock is authoritative',420,390,300,90),('resolve','Outcome','Commit if active / void if expired',855,390,300,90),('manual','Manual review','No fabricated success on timeout',35,390,285,90)], [('timeout','unknown','transport fault'),('unknown','lookup','reconcile'),('lookup','active','authorized'),('active','resolve','yes/no'),('lookup','manual','irreconcilable')],doc='operations/runbooks/payment-unknown.md')
graph('failure-restore','Failure/recovery — isolated multi-owner restore','Failure',[
 ('cut','Checkpoint manifest','Quiesce / per-owner snapshot times',35,130,290,90),('restore','Isolated restore','Validate checksums/grants/schema',420,130,310,90),('audit','Owner invariant audit','Counts • overlaps • ledger bounds',855,130,300,90),('provider','PSP reconciliation','Provider keys may postdate backup',420,390,310,90),('resume','Resume controlled traffic','Consumers/outbox after verification',855,390,300,90),('report','Delta report','Measured RPO/RTO and losses',35,390,290,90)], [('cut','restore','snapshots'),('restore','audit','no traffic'),('audit','provider','known states'),('provider','resume','reconciled'),('resume','report','evidence')],doc='operations/backup-recovery.md')
graph('booking-state','Booking state — guarded transitions','State',[
 ('pending','PENDING','Hold → authorization → commit',40,125,270,90),('confirmed','CONFIRMED','Only after committed + authorized',460,125,280,90),('claim','HANDOVER_CLAIMED','Atomic cancellation fence',900,125,290,90),('cancel','CANCELLING / COMPENSATING','Release + full void evidence',40,355,320,90),('terminal','CANCELLED / FAILED','Late events still compensated',40,570,320,90),('inuse','IN_USE','Physical handover fact',900,355,290,90),('settle','SETTLING','Return + release → capture/void',460,355,300,90),('complete','COMPLETED / MANUAL_REVIEW','Funds known / explicit unresolved',460,570,370,90)], [('pending','confirmed','commit proof'),('pending','cancel','expiry/cancel'),('confirmed','cancel','cancel wins'),('confirmed','claim','claim wins'),('claim','inuse','handover fact'),('cancel','terminal','compensated'),('inuse','settle','returned'),('settle','complete','settlement evidence')],doc='product/business-processes.md',height=720)
for slug,title,labels in [('customer-flow','Customer journey',['Catalog','Availability','Quote','Checkout','Pending','Booking / cancel','Settlement']),('warehouse-flow','Warehouse journey',['Depot jobs','Job details','Handover claim','Physical inspection','Return','Quarantine / repair','Finance review'])]:
    nd=[(str(i),l,'Concrete screen / state',40+(i%4)*295,130+(i//4)*250,240,90) for i,l in enumerate(labels)]
    graph(slug,title,'User flow',nd,[(str(i),str(i+1),'next') for i in range(len(labels)-1)],doc='design/design-spec.md')
for tr in tracks:
    nodes=[(n['milestone'],n['milestone']+' • '+n['label'][:22],n['practice'][:33]+'|Proof in assignment',40+(i%3)*400,125+(i//3)*240,350,95) for i,n in enumerate(tr['nodes'])]
    graph('roadmap-'+tr['slug'],tr['name']+' roadmap','Roadmap',nodes,[(nodes[i][0],nodes[i+1][0],'next checkpoint') for i in range(len(nodes)-1)],doc='roadmaps/'+tr['slug']+'.md',width=1250,height=700 if len(nodes)>3 else 450)
# The project diagram shows every milestone, while individual skill tracks use checkpoints.
project_nodes=[]
for i,m in enumerate(milestones):
    row,col=divmod(i,3)
    if row%2:col=2-col
    project_nodes.append((m['id'],m['id']+' • '+m['title'][:27],m['skills'][:40],40+col*400,120+row*200,350,95))
old=next(d for d in DIAGRAMS if d['id']=='roadmap-project');DIAGRAMS.remove(old)
graph('roadmap-project','Project roadmap — all 18 prerequisites','Roadmap',project_nodes,[(m['depends'][0],m['id'],'prerequisite') for m in milestones if m['depends']],doc='roadmaps/project.md',width=1250,height=1400)
# Replace the dense container graph with an explicitly routed bus layout.
container_source=dict(title='Container diagram — seven owned business boundaries',width=2040,height=1060,services=[s['id'] for s in SERVICES],http_bus='gateway to public endpoints; owner-to-owner GETs in sequence diagrams',amqp_bus='commands/events, per-consumer queue and own ACL',infra=['React','Gateway','Keycloak','RabbitMQ','Redis','OTel/Grafana','SandboxPSP','Mail sink'],private_databases='one per owner; no cross-SQL')
out=head(2040,1060,container_source['title'])
def box(x,y,w,label,desc,service='',h=90):
    return f'<g data-service="{service}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#20364a" stroke="{ "#efab58" if service else "#527189"}"/>'+svg_text(x+15,y+31,label,17)+''.join(svg_text(x+15,y+55+j*17,l,12,'#a8bdce') for j,l in enumerate(desc.split('|')))+'</g>'
out+=box(40,110,280,'React / TypeScript','Browser; role-based UI')+box(390,110,280,'Gateway / Nginx','TLS • routing • rate limits')+box(740,110,280,'Keycloak','OIDC • PKCE • JWKS')+box(1090,110,350,'OTel / Grafana stack','Metrics • logs • traces')+box(1510,110,450,'Sandbox PSP / mail sink','Billing or Notification adapter only')
out+='<path d="M320 155 H390" stroke="#68cbd4" marker-end="url(#arr)"/><path d="M180 110 V92 H880 V110" stroke="#68cbd4" fill="none" marker-end="url(#arr)"/>'+svg_text(520,88,'PKCE',12)
out+='<path d="M530 200 V270 H1960 M40 270 H530" stroke="#68cbd4" fill="none" stroke-width="2"/>'+svg_text(45,252,'HTTPS business API bus — JWT verified at each service; internal GET/claims described in contracts',15,'#68cbd4')
for i,s in enumerate(SERVICES):
    x=40+i*280
    out+=f'<path d="M{x+115} 270 V340" stroke="#68cbd4" marker-end="url(#arr)"/>'+box(x,340,230,s['name'],'Own image • own API|'+('Node / TypeScript' if s['id']=='notification' else 'Java / Spring Boot'),s['id'])
    out+=f'<path d="M{x+115} 430 V490" stroke="#efab58" marker-end="url(#arr)"/>'+svg_text(x+120,465,'owner SQL',12,'#efab58')+box(x,490,230,s['name']+' DB','Private PostgreSQL|Own app/migration role',h=90)
    # AMQP connection runs beside the private DB, never through a foreign table.
    out+=f'<path d="M{x+230} 394 H{x+250} V650" stroke="#68cbd4" fill="none" stroke-dasharray="6 4"/>'
out+='<path d="M40 650 H1970" stroke="#68cbd4" stroke-width="2"/>'+svg_text(45,628,'AMQP event/command bus — durable outbox/inbox, at-least-once, explicit per-owner contracts',15,'#68cbd4')
out+='<path d="M220 650 V730" stroke="#68cbd4" marker-end="url(#arr)"/>'+box(40,730,410,'RabbitMQ','commands + facts + DLQ|1node dev / 3node quorum lab',h=100)
out+=box(540,730,410,'Redis','Catalog list cache + gateway throttle|Not an allocation or auth authority',h=100)
out+=box(1040,730,410,'Owned backup / restore','Snapshot manifest + reconciliation|Independent isolated restore target',h=100)
out+=box(1540,730,420,'Independent deployment','7images • 7migrations • contract gates|Compose → production-like K8s',h=100)
out+=svg_text(40,900,'Dashed AMQP lines are logical message routes. SQL arrows terminate only in the owner database.',17)
out+=svg_text(40,935,'HTTP Tenancy checks, Fulfillment claim/eligibility and Billing PSP lookup are sync; reservation saga messages are async.',17)
out+=svg_text(40,970,'Supporting cache/telemetry/backup paths are defined in Network and Observability diagrams; infrastructure is not counted as business services.',15)
out+='</svg>'
write('architecture/diagrams/containers.svg',out);dump('architecture/diagrams/containers.json',container_source)
item=next(d for d in DIAGRAMS if d['id']=='containers');item['svg']=out
dump('architecture/diagrams/index.json',[{k:v for k,v in d.items() if k!='svg'} for d in DIAGRAMS])
dump('atlas/diagrams.json',DIAGRAMS)
write('atlas/diagrams.js','window.DIAGRAMS = '+json.dumps(DIAGRAMS,ensure_ascii=False)+';')
write('design/design-spec.md', '''# Product design specification — DepotFlow

Visual prototype: design/prototype.html; entirely offline, synthetic data and simulated state. It is a reference for independent React implementation, not the backend. Screens mapped in screens.json to F/M IDs. Editable HTML/CSS/JS source and rendered SVG architecture diagrams supplied; Figma unnecessary.

## Information architecture / journeys

Customer: catalog → availability → quote → checkout → pending → booking detail → cancel or settlement; notifications accessible from header. Operator: warehouse jobs → handover inspection → return → fleet/quarantine → maintenance. Finance: payment list → ledger → refund/manual review. Admin: team → role/depot assignment → catalog/rates → audit. Login/denied common. Role selector is a demonstration control, not authentication. Switch to role before screen; permissions enforced later in API.

## Design system

Palette: canvas#f4f6f7, ink#132a39, muted#526570, border#d4dfe4, brand#075d64, accent#b45512, danger#b42318, surface#ffffff, focus#1d70b8. Typography system Segoe UI/Arial offline; body16px line1.55, headings32/24/18px; tabular money/numbers. Spacing4/8/12/16/24/32; radius12 cards,8inputs/buttons; max content1240px; desktop sidebar232px + fluid main; mobile bottom-friendly full-width actions, single column≤720px. Customer forms put price/status alongside desktop, below on mobile; sticky summary never hides field focus.

Components: labeled text/date/qty/money field + help/error IDs; button primary/secondary/danger/loading disabled; breadcrumb; badge with text; table with header/empty/loading pagination; filter bar; status timeline; confirmation dialog; alert role/status aria-live; accessible tabs; progress indicator; notification card; code/correlation ID; responsive asset checklist. Dialog traps focus/escape closes and restores trigger in student implementation. Prototype uses inline review/confirm screen instead of inaccessible faux modal.

## State specification

Loading: skeleton or labeled progress, preserve layout, no duplicate submit. Empty: catalog suggests clear filters; warehouse says no pending jobs, no fake success. Error: stable problem code, correlation and retry safe only per operation ID. Unauthorized: login action401; denied403 explains required role/depot without foreign data. Quote expired: refresh and compare changed amount, requires user consent. Pending: outcome unknown, no success badge; manual review has explanation and contact operator. Success: confirmed only on allocation+auth proof; refund pending until authoritative event. Offline/SSE stale: updated_at banner plus snapshot recovery, never replay checkout automatically.

Accessibility target N09: WCAG-oriented keyboard journeys, explicit labels/errors, visible focus, no color-only statuses, text contrast≥4.5:1, reduced motion; touch targets≥44px. Implementation audit checks real assistive behavior; prototype visual QA is not certification. Tables scroll within region on narrow screens, no document horizontal overflow. Notification includes textual changed state rather than animation.

Screen / acceptance mapping screens.json; prototype controls navigate all screens and demonstrate loading/empty/error/success/denied/reconnecting. Prices/entities labeled demo; sample booking confirmed only by explicit simulated advance action. Persistent project progress belongs atlas, not business state. No forms send network requests.
''')
SCREENS=[
 ('login','Вход','customer',['F01'],'M02'),('catalog','Каталог','customer',['F02','F03'],'M11'),('availability','Наличие на срок','customer',['F03','F05'],'M11'),('quote','Котировка','customer',['F04'],'M11'),('checkout','Проверка аренды','customer',['F04','F07'],'M11'),('pending','Подтверждение в процессе','customer',['F05','F06','F18'],'M11'),('booking','Аренда DF-1042','customer',['F06','F08','F15'],'M11'),('cancel','Отмена аренды','customer',['F08'],'M11'),('notifications','Уведомления','customer',['F14'],'M11'),('warehouse','Работа склада','operator',['F09'],'M09'),('handover','Выдача оборудования','operator',['F09'],'M09'),('return','Возврат и осмотр','operator',['F10'],'M09'),('fleet','Парк оборудования','operator',['F13','F16'],'M04'),('maintenance','Ремонт','operator',['F13','F16'],'M04'),('billing','Расчёты / ledger','finance',['F11','F12'],'M10'),('refund','Возврат средств','finance',['F12'],'M10'),('team','Команда и доступ','org_admin',['F01'],'M02'),('rate','Тарифы моделей','org_admin',['F02','F04'],'M03'),('audit','Журнал действий','org_admin',['F15'],'M12'),('operations','Операционный incident','operator',['F18','F19','F20'],'M14'),('denied','Доступ запрещён','customer',['F01'],'M02'),('contracts','Контракты','org_admin',['F17'],'M13')]
dump('design/screens.json',[dict(id=i,title=t,role=r,requirements=f,milestone=m,route='prototype.html#'+i,states=['normal','loading','empty','error','success','denied','reconnecting']) for i,t,r,f,m in SCREENS])
write('design/screens.js','window.SCREENS = '+json.dumps([dict(id=i,title=t,role=r,requirements=f,milestone=m) for i,t,r,f,m in SCREENS],ensure_ascii=False)+';')
if __name__=='__main__': finish_registry();print('Rendered diagrams:',len(DIAGRAMS))

