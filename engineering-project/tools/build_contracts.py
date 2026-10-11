from build_content import *
UUID={'type':'string','format':'uuid'}
TIME={'type':'string','format':'date-time'}
MONEY={'type':'integer','minimum':0,'maximum':9000000000000}
TEXT={'type':'string','minLength':1,'maxLength':120}
def enum(*vals): return {'type':'string','enum':list(vals)}
def obj(props,required=None): return {'type':'object','properties':props,'required':required if required is not None else list(props),'additionalProperties':False}
def ref(name): return {'$ref':'#/components/schemas/'+name}
SCHEMAS={
 'Problem':obj({'type':{'type':'string'},'title':TEXT,'status':{'type':'integer'},'code':TEXT,'correlationId':UUID,'violations':{'type':'array','items':obj({'path':TEXT,'message':TEXT})}},['type','title','status','code','correlationId']),
 'Accepted':obj({'operation_id':UUID,'resource_id':UUID,'status':TEXT,'status_url':{'type':'string','format':'uri-reference'}}),
 'Membership':obj({'id':UUID,'org_id':UUID,'subject_id':TEXT,'role':enum('customer','operator','finance','org_admin'),'depot_id':UUID,'status':enum('active','revoked'),'version':{'type':'integer','minimum':1}},['id','org_id','subject_id','role','status','version']),
 'MembershipInput':obj({'subject_id':TEXT,'role':enum('customer','operator','finance','org_admin'),'depot_id':UUID},['subject_id','role']),
 'Model':obj({'id':UUID,'org_id':UUID,'name':TEXT,'category':TEXT,'active':{'type':'boolean'},'version':{'type':'integer','minimum':1}}),
 'ModelInput':obj({'name':TEXT,'category':TEXT}),
 'RateInput':obj({'daily_minor':MONEY,'deposit_minor':MONEY,'currency':enum('EUR'),'valid_from':TIME}),
 'Rate':obj({'id':UUID,'model_id':UUID,'version':{'type':'integer','minimum':1},'daily_minor':MONEY,'deposit_minor':MONEY,'currency':enum('EUR'),'valid_from':TIME}),
 'QuoteInput':obj({'model_id':UUID,'depot_id':UUID,'start_at':TIME,'end_at':TIME,'quantity':{'type':'integer','minimum':1,'maximum':5}}),
 'Quote':obj({'id':UUID,'org_id':UUID,'model_id':UUID,'depot_id':UUID,'start_at':TIME,'end_at':TIME,'quantity':{'type':'integer','minimum':1,'maximum':5},'days':{'type':'integer','minimum':1,'maximum':30},'daily_minor':MONEY,'rental_minor':MONEY,'deposit_minor':MONEY,'currency':enum('EUR'),'rate_version':{'type':'integer','minimum':1},'expires_at':TIME}),
 'Availability':obj({'model_id':UUID,'depot_id':UUID,'quantity_available':{'type':'integer','minimum':0},'authoritative_at':TIME,'guaranteed':enum('no')}),
 'Depot':obj({'id':UUID,'org_id':UUID,'name':TEXT,'timezone':enum('Europe/Tallinn')}),
 'Asset':obj({'id':UUID,'org_id':UUID,'model_id':UUID,'depot_id':UUID,'serial':TEXT,'state':enum('READY','RENTED','QUARANTINED','UNAVAILABLE'),'version':{'type':'integer','minimum':1}}),
 'AssetInput':obj({'model_id':UUID,'depot_id':UUID,'serial':TEXT}),
 'AssetUpdate':obj({'serial':TEXT}),
 'MaintenanceInput':obj({'asset_id':UUID,'start_at':TIME,'end_at':TIME,'reason':{'type':'string','minLength':1,'maxLength':1000}}),
 'Maintenance':obj({'id':UUID,'asset_id':UUID,'status':enum('OPEN','COMPLETED'),'version':{'type':'integer','minimum':1}}),
 'Reason':obj({'reason':{'type':'string','minLength':1,'maxLength':1000}}),
 'Hold':obj({'id':UUID,'booking_id':UUID,'asset_ids':{'type':'array','items':UUID,'minItems':1,'maxItems':5},'expires_at':TIME,'status':enum('HELD','COMMITTED','RELEASED','EXPIRED'),'version':{'type':'integer','minimum':1}}),
 'HandoverEligibility':obj({'booking_id':UUID,'asset_ids':{'type':'array','items':UUID},'eligible':{'type':'boolean'},'checked_at':TIME,'reason':enum('ready','unavailable','overrun','quarantined','allocation_missing')}),
 'BookingInput':obj({'quote_id':UUID}),
 'Booking':obj({'id':UUID,'org_id':UUID,'customer_id':TEXT,'quote_id':UUID,'status':enum('PENDING','CONFIRMED','COMPENSATING','CANCELLING','CANCELLED','FAILED','HANDOVER_CLAIMED','IN_USE','SETTLING','COMPLETED','MANUAL_REVIEW'),'version':{'type':'integer','minimum':1},'updated_at':TIME,'quote_snapshot':ref('Quote'),'asset_ids':{'type':'array','items':UUID},'depot_id':UUID},['id','org_id','customer_id','quote_id','status','version','updated_at','quote_snapshot']),
 'ClaimInput':obj({'job_id':UUID,'asset_ids':{'type':'array','items':UUID,'minItems':1,'maxItems':5}}),
 'Claim':obj({'claim_id':UUID,'booking_id':UUID,'job_id':UUID,'state':enum('HANDOVER_CLAIMED','IN_USE'),'claimed_at':TIME,'version':{'type':'integer','minimum':1}}),
 'TimelineEntry':obj({'id':UUID,'type':TEXT,'source_event_id':UUID,'at':TIME,'summary':{'type':'string','maxLength':500}}),
 'Intent':obj({'id':UUID,'booking_id':UUID,'authorized_minor':MONEY,'captured_minor':MONEY,'refunded_minor':MONEY,'pending_refund_minor':MONEY,'remaining_authorization_minor':MONEY,'status':enum('PENDING','AUTHORIZED','UNKNOWN','DECLINED','VOIDED','CAPTURED','PARTIALLY_REFUNDED','REFUNDED','MANUAL_REVIEW'),'version':{'type':'integer','minimum':1}}),
 'RefundInput':obj({'amount_minor':MONEY,'reason':{'type':'string','minLength':1,'maxLength':1000}}),
 'Webhook':obj({'provider_event_id':UUID,'operation_id':UUID,'provider_key':TEXT,'intent_id':UUID,'result':enum('authorized','declined','voided','captured','refunded'),'amount_minor':MONEY,'occurred_at':TIME}),
 'LedgerEntry':obj({'id':UUID,'intent_id':UUID,'operation_id':UUID,'kind':enum('AUTHORIZE','CAPTURE','VOID','REFUND'),'amount_minor':MONEY,'created_at':TIME}),
 'Job':obj({'id':UUID,'booking_id':UUID,'depot_id':UUID,'status':enum('READY','HANDOVER_CLAIMED','IN_USE','RETURNED','CANCELLED','BLOCKED'),'asset_ids':{'type':'array','items':UUID},'version':{'type':'integer','minimum':1},'updated_at':TIME}),
 'HandoverInput':obj({'asset_ids':{'type':'array','items':UUID,'minItems':1,'maxItems':5},'inspection_ok':{'type':'boolean','const':True}}),
 'Handover':obj({'id':UUID,'job_id':UUID,'claim_id':UUID,'asset_ids':{'type':'array','items':UUID},'occurred_at':TIME}),
 'ReturnInput':obj({'condition':enum('good','damaged'),'damage_minor':MONEY,'notes':{'type':'string','maxLength':1000}}),
 'Return':obj({'id':UUID,'job_id':UUID,'condition':enum('good','damaged'),'damage_minor':MONEY,'late_days':{'type':'integer','minimum':0},'returned_at':TIME,'version':{'type':'integer','minimum':1}}),
 'Notification':obj({'id':UUID,'title':TEXT,'source_event_id':UUID,'created_at':TIME,'read_at':{'type':['string','null'],'format':'date-time'}}),
 'PreferenceInput':obj({'email_enabled':{'type':'boolean'}}),
 'Preference':obj({'subject_id':TEXT,'email_enabled':{'type':'boolean'},'version':{'type':'integer','minimum':1}}),
 'AuditEntry':obj({'id':UUID,'actor_id':TEXT,'action':TEXT,'target_id':UUID,'occurred_at':TIME})
}
# Positive charge/rate/refund amounts; deposits and balances may be zero.
for schema_name,field_name in [('RateInput','daily_minor'),('Rate','daily_minor'),('Quote','daily_minor'),('RefundInput','amount_minor')]:
    SCHEMAS[schema_name]['properties'][field_name]={**MONEY,'minimum':1}
# service, method, path, summary, in_schema, out_schema, success, roles, requirement, internal, etag
OPS = [
 ('tenancy','get','/v1/membership','Current user membership',None,'Membership',200,['customer','operator','finance','org_admin'],'F01',False,False),
 ('tenancy','post','/v1/memberships','Invite/assign membership','MembershipInput','Membership',201,['org_admin'],'F01',False,False),
 ('tenancy','patch','/v1/memberships/{id}','Change role/depot','MembershipInput','Membership',200,['org_admin'],'F01',False,True),
 ('tenancy','delete','/v1/memberships/{id}','Revoke membership',None,None,204,['org_admin'],'F01',False,True),
 ('tenancy','get','/v1/audit','Audit entries',None,'AuditEntry[]',200,['org_admin'],'F15',False,False),
 ('tenancy','get','/internal/v1/memberships/{subject_id}','Authoritative mutation permission',None,'Membership',200,['service'],'F01',True,False),
 ('catalog','get','/v1/models','Search paginated model catalog',None,'Model[]',200,['customer','operator','org_admin'],'F03',False,False),
 ('catalog','post','/v1/models','Create active model','ModelInput','Model',201,['org_admin'],'F02',False,False),
 ('catalog','post','/v1/models/{id}/rates','Create immutable versioned rate','RateInput','Rate',201,['org_admin'],'F02',False,False),
 ('catalog','post','/v1/models/{id}/deactivate','Stop issuing new quotes','Reason','Model',200,['org_admin'],'F02',False,True),
 ('catalog','post','/v1/quotes','Create immutable quote','QuoteInput','Quote',201,['customer'],'F04',False,False),
 ('catalog','get','/v1/quotes/{id}','Own tenant quote',None,'Quote',200,['customer','org_admin'],'F04',False,False),
 ('catalog','get','/internal/v1/quotes/{id}','Booking quote snapshot lookup',None,'Quote',200,['booking'],'F04',True,False),
 ('inventory','get','/v1/availability','Indicative temporal availability',None,'Availability',200,['customer','operator'],'F03',False,False),
 ('inventory','get','/v1/assets','Depot asset list',None,'Asset[]',200,['operator','org_admin'],'F13',False,False),
 ('inventory','post','/v1/assets','Register asset','AssetInput','Asset',201,['operator'],'F13',False,False),
 ('inventory','patch','/v1/assets/{id}','Edit asset metadata','AssetUpdate','Asset',200,['operator'],'F16',False,True),
 ('inventory','post','/v1/maintenance','Block asset for repair','MaintenanceInput','Maintenance',201,['operator'],'F13',False,False),
 ('inventory','post','/v1/maintenance/{id}/complete','Complete repair inspection','Reason','Maintenance',200,['operator'],'F13',False,True),
 ('inventory','get','/internal/v1/holds/by-booking/{booking_id}','Recover authoritative hold outcome',None,'Hold',200,['booking'],'F18',True,False),
 ('inventory','get','/internal/v1/depots/{id}','Validate membership depot',None,'Depot',200,['tenancy'],'F01',True,False),
 ('inventory','get','/internal/v1/bookings/{booking_id}/handover-check','Current physical eligibility and committed allocation',None,'HandoverEligibility',200,['fulfillment'],'F09',True,False),
 ('booking','post','/v1/bookings','Start asynchronous reservation','BookingInput','Accepted',202,['customer'],'F05',False,False),
 ('booking','get','/v1/bookings','Own bookings or authorized organization jobs',None,'Booking[]',200,['customer','operator','org_admin'],'F06',False,False),
 ('booking','get','/v1/bookings/{id}','Authoritative status and snapshot',None,'Booking',200,['customer','operator','finance','org_admin'],'F06',False,False),
 ('booking','get','/v1/bookings/{id}/timeline','Rental event timeline',None,'TimelineEntry[]',200,['customer','org_admin'],'F15',False,False),
 ('booking','post','/v1/bookings/{id}/cancel','Record cancellation intent','Reason','Accepted',202,['customer','org_admin'],'F08',False,True),
 ('booking','post','/internal/v1/bookings/{id}/handover-claim','Fence physical handover','ClaimInput','Claim',200,['fulfillment'],'F09',True,True),
 ('booking','get','/internal/v1/bookings/{id}','Warehouse authoritative state',None,'Booking',200,['fulfillment'],'F09',True,False),
 ('booking','get','/internal/v1/claims/by-job/{job_id}','Recover ambiguous handover claim',None,'Claim',200,['fulfillment'],'F18',True,False),
 ('billing','get','/v1/payments/by-booking/{booking_id}','Tenant/customer payment status',None,'Intent',200,['customer','finance'],'F11',False,False),
 ('billing','get','/v1/payments/{id}/ledger','Immutable ledger history',None,'LedgerEntry[]',200,['finance'],'F11',False,False),
 ('billing','post','/v1/payments/{id}/refunds','Reserve refund and request sandbox operation','RefundInput','Accepted',202,['finance'],'F12',False,True),
 ('billing','post','/callbacks/v1/psp','Signed sandbox webhook','Webhook',None,204,['provider'],'F11',True,False),
 ('billing','get','/internal/v1/payments/by-booking/{booking_id}','Saga payment recovery status',None,'Intent',200,['booking'],'F18',True,False),
 ('fulfillment','get','/v1/jobs','Depot workload cursor list',None,'Job[]',200,['operator'],'F09',False,False),
 ('fulfillment','get','/v1/jobs/{id}','Job details',None,'Job',200,['operator'],'F09',False,False),
 ('fulfillment','post','/v1/jobs/{id}/handover','Claim and record physical inspection','HandoverInput','Handover',201,['operator'],'F09',False,True),
 ('fulfillment','post','/v1/jobs/{id}/return','Record all-assets inspection return','ReturnInput','Return',201,['operator'],'F10',False,True),
 ('notification','get','/v1/notifications','Current user notifications',None,'Notification[]',200,['customer','operator','finance','org_admin'],'F14',False,False),
 ('notification','post','/v1/notifications/{id}/read','Mark own notification read',None,'Notification',200,['customer','operator','finance','org_admin'],'F14',False,False),
 ('notification','get','/v1/notifications/stream','SSE replay with Last-Event-ID',None,'SSE',200,['customer','operator','finance','org_admin'],'F14',False,False),
 ('notification','get','/v1/preferences','Own channel settings',None,'Preference',200,['customer'],'F14',False,False),
 ('notification','put','/v1/preferences','Change channel settings','PreferenceInput','Preference',200,['customer'],'F14',False,True)
]
def response_schema(out):
    if out.endswith('[]'):
        return obj({'items':{'type':'array','items':ref(out[:-2])},'next_cursor':{'type':['string','null']},'updated_at':TIME})
    return ref(out)
for s in SERVICES:
    paths={}
    for service,method,path,summary,inp,out,code,roles,rid,internal,etag in OPS:
        if service!=s['id']: continue
        ps=[]
        for param in re.findall(r'\{([^}]+)\}',path): ps.append(dict(name=param,**{'in':'path'},required=True,schema=TEXT if param=='subject_id' else UUID))
        if internal and '/callbacks/' not in path:
            ps += [dict(name='X-Org-ID',**{'in':'header'},required=True,schema=UUID),dict(name='X-Subject-ID',**{'in':'header'},required=True,schema=TEXT)]
        if method!='get' and '/callbacks/' not in path:
            ps.append(dict(name='Idempotency-Key',**{'in':'header'},required=True,schema={'type':'string','minLength':8,'maxLength':128}))
        if etag: ps.append(dict(name='If-Match',**{'in':'header'},required=True,schema={'type':'string','pattern':'^"[0-9]+"$'}))
        if method=='get' and out and out.endswith('[]'):
            ps += [dict(name='cursor',**{'in':'query'},schema={'type':'string','maxLength':512}),dict(name='limit',**{'in':'query'},schema={'type':'integer','minimum':1,'maximum':100,'default':25})]
        if path=='/v1/models': ps += [dict(name='q',**{'in':'query'},schema={'type':'string','maxLength':120}),dict(name='category',**{'in':'query'},schema=TEXT)]
        if path=='/v1/availability': ps += [dict(name=n,**{'in':'query'},required=True,schema=t) for n,t in [('model_id',UUID),('depot_id',UUID),('start_at',TIME),('end_at',TIME),('quantity',{'type':'integer','minimum':1,'maximum':5})]]
        if path in ['/v1/bookings','/v1/jobs','/v1/assets'] and method=='get': ps += [dict(name='status' if path!='/v1/assets' else 'state',**{'in':'query'},schema=TEXT),dict(name='depot_id',**{'in':'query'},schema=UUID)]
        if out=='SSE': ps.append(dict(name='Last-Event-ID',**{'in':'header'},schema=UUID))
        if '/callbacks/' in path: ps += [dict(name=n,**{'in':'header'},required=True,schema=TEXT) for n in ['X-PSP-Signature','X-PSP-Timestamp']]
        resp={str(code):{'description':summary}}
        if out:
            resp[str(code)]['content']={'text/event-stream' if out=='SSE' else 'application/json':{'schema':{'type':'string','description':'id UUID; event notification; data validated Notification JSON. Last-Event-ID replays retained cursor; missing cursor triggers snapshot.'} if out=='SSE' else response_schema(out)}}
            if out!='SSE': resp[str(code)]['headers']={'ETag':{'schema':{'type':'string'},'description':'Quoted version for mutable resources; absent for immutable quote/list.'}}
        for ec in [401,403,404,409,412,422,428,429,503]: resp[str(ec)]={'description':{401:'invalid_auth',403:'forbidden',404:'not_found',409:'business_conflict or idempotency_mismatch',412:'stale_version',422:'validation_failed',428:'precondition_required',429:'rate_limited',503:'dependency_unavailable'}[ec],'content':{'application/problem+json':{'schema':ref('Problem')}}}
        op=dict(operationId=s['id']+'_'+method+'_'+re.sub(r'[^a-zA-Z0-9]+','_',path).strip('_'),summary=summary,tags=['internal' if internal else 'public'],parameters=ps,responses=resp,security=[{'pspSignature':[]} if '/callbacks/' in path else {'serviceBearer' if internal else 'userBearer':[]}],**{'x-roles':roles,'x-requirement':rid,'x-authorization':'Derive org from membership; customer own resource only; operator assigned depot; internal scope plus original subject. Never trust arbitrary org header.'})
        if inp: op['requestBody']={'required':True,'content':{'application/json':{'schema':ref(inp)}}}
        paths.setdefault(path,{})[method]=op
    dump(f"contracts/openapi/{s['id']}.json",dict(openapi='3.1.1',info=dict(title='DepotFlow '+s['name'],version='1.0.0',description='Design contract; no running backend supplied. See business rules and authorization matrix.'),servers=[dict(url='https://'+s['id']+'.lab.invalid',description='Placeholder lab service DNS, configure implementation gateway routes')],paths=paths,components=dict(securitySchemes={'userBearer':{'type':'http','scheme':'bearer','bearerFormat':'JWT'},'serviceBearer':{'type':'http','scheme':'bearer','bearerFormat':'JWT'},'pspSignature':{'type':'apiKey','in':'header','name':'X-PSP-Signature'}},schemas=SCHEMAS)))

EVENT_DATA={
 'membership.changed':obj({'membership_id':UUID,'subject_id':TEXT,'role':enum('customer','operator','finance','org_admin'),'status':enum('active','revoked'),'depot_id':UUID},['membership_id','subject_id','role','status']),
 'catalog.changed':obj({'model_id':UUID,'rate_version':{'type':'integer','minimum':1},'active':{'type':'boolean'}}),
 'booking.reserve-requested':obj({'booking_id':UUID,'customer_id':TEXT,'quote':ref('Quote'),'command_id':UUID,'deadline_at':TIME}),
 'hold.created':obj({'booking_id':UUID,'hold_id':UUID,'asset_ids':{'type':'array','items':UUID,'minItems':1,'maxItems':5},'expires_at':TIME}),
 'hold.rejected':obj({'booking_id':UUID,'reason':enum('insufficient_assets','cancelled_tombstone','invalid_interval','deadline_expired')}),
 'hold.expired':obj({'booking_id':UUID,'hold_id':UUID,'expired_at':TIME}),
 'booking.commit-requested':obj({'booking_id':UUID,'hold_id':UUID,'intent_id':UUID,'command_id':UUID}),
 'allocation.committed':obj({'booking_id':UUID,'hold_id':UUID,'asset_ids':{'type':'array','items':UUID,'minItems':1,'maxItems':5}}),
 'booking.release-requested':obj({'booking_id':UUID,'command_id':UUID,'reason':enum('cancel','expiry','failed','return')}),
 'allocation.released':obj({'booking_id':UUID,'reason':enum('cancel','expiry','failed','return'),'tombstone':{'type':'boolean'}}),
 'asset.unavailable':obj({'asset_id':UUID,'reason':enum('overrun','damage','maintenance'),'affected_booking_ids':{'type':'array','items':UUID}}),
 'billing.authorize-requested':obj({'booking_id':UUID,'customer_id':TEXT,'amount_minor':MONEY,'currency':enum('EUR'),'command_id':UUID,'deadline_at':TIME}),
 'payment.authorized':obj({'booking_id':UUID,'intent_id':UUID,'authorized_minor':MONEY,'authorization_expires_at':TIME}),
 'payment.failed':obj({'booking_id':UUID,'intent_id':UUID,'reason':enum('declined','provider_expired','validation_failed')}),
 'billing.void-requested':obj({'booking_id':UUID,'command_id':UUID,'reason':enum('cancel','expiry','unused_authorization')}),
 'payment.voided':obj({'booking_id':UUID,'intent_id':UUID,'operation_id':UUID,'voided_minor':MONEY,'remaining_authorization_minor':MONEY,'kind':enum('full','remainder')}),
 'billing.settle-requested':obj({'booking_id':UUID,'intent_id':UUID,'command_id':UUID,'return_report_id':UUID,'capture_minor':MONEY,'currency':enum('EUR')}),
 'payment.captured':obj({'booking_id':UUID,'intent_id':UUID,'operation_id':UUID,'captured_minor':MONEY}),
 'payment.refunded':obj({'booking_id':UUID,'intent_id':UUID,'operation_id':UUID,'refunded_minor':MONEY,'customer_id':TEXT}),
 'booking.confirmed':obj({'booking_id':UUID,'customer_id':TEXT,'depot_id':UUID,'asset_ids':{'type':'array','items':UUID,'minItems':1,'maxItems':5},'quote':ref('Quote')}),
 'booking.cancelled':obj({'booking_id':UUID,'customer_id':TEXT,'reason':TEXT}),
 'fulfillment.handed-over':obj({'booking_id':UUID,'job_id':UUID,'claim_id':UUID,'asset_ids':{'type':'array','items':UUID},'handed_over_at':TIME}),
 'fulfillment.returned':obj({'booking_id':UUID,'job_id':UUID,'return_report_id':UUID,'asset_ids':{'type':'array','items':UUID},'customer_id':TEXT,'condition':enum('good','damaged'),'damage_minor':MONEY,'late_days':{'type':'integer','minimum':0},'returned_at':TIME})
}
# Additional consumers required by explicit overrun rule and settlement acknowledgement.
next(s for s in SERVICES if s['id']=='booking')['consumes'] += ['asset.unavailable']
next(s for s in SERVICES if s['id']=='fulfillment')['consumes'] += ['asset.unavailable']
next(s for s in SERVICES if s['id']=='catalog')['consumes'] += ['catalog.changed']
for s in SERVICES:
    channels={}; operations={}
    for ev in sorted(set(s['publishes']+s['consumes'])):
        channel_key=ev.replace('.','_').replace('-','_')
        producer=next(x['id'] for x in SERVICES if ev in x['publishes'])
        schema=obj({'event_id':UUID,'type':{'type':'string','const':ev+'.v1'},'schema_version':{'type':'integer','const':1},'producer':{'type':'string','const':producer},'org_id':UUID,'aggregate_id':UUID,'aggregate_version':{'type':'integer','minimum':1},'occurred_at':TIME,'correlation_id':UUID,'causation_id':UUID,'traceparent':{'type':'string','pattern':'^[0-9a-f]{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$'},'data':EVENT_DATA[ev]},['event_id','type','schema_version','producer','org_id','aggregate_id','aggregate_version','occurred_at','correlation_id','causation_id','data'])
        channels[channel_key]={'address':ev+'.v1','messages':{'event':{'name':ev+'.v1','title':ev,'contentType':'application/json','payload':schema,'correlationId':{'location':'$message.payload#/correlation_id'}}},'description':f"{'Command to sole owner' if ev.endswith('requested') else 'Domain fact'}; producer={producer}; consumers={','.join(x['id'] for x in SERVICES if ev in x['consumes'])}"}
        for action,events in [('send',s['publishes']),('receive',s['consumes'])]:
            if ev in events: operations[action+'_'+channel_key]={'action':action,'channel':{'$ref':'#/channels/'+channel_key},'messages':[{'$ref':'#/channels/'+channel_key+'/messages/event'}]}
    dump(f"contracts/asyncapi/{s['id']}.json",{'asyncapi':'3.0.0','info':{'title':'DepotFlow '+s['name']+' messaging','version':'1.0.0'},'defaultContentType':'application/json','servers':{'lab':{'host':'rabbitmq.lab.invalid:5671','protocol':'amqp','protocolVersion':'0.9.1','description':'TLS, ACL per service; topology in messaging-topology.json'}},'channels':channels,'operations':operations,'components':{'schemas':SCHEMAS}})
    # standalone event schemas carry Quote components for internal refs
for ev,data in EVENT_DATA.items():
    producer=next(s['id'] for s in SERVICES if ev in s['publishes'])
    aa=json.loads((ROOT/f'contracts/asyncapi/{producer}.json').read_text(encoding='utf-8'))
    key=ev.replace('.','_').replace('-','_'); sc=aa['channels'][key]['messages']['event']['payload']
    sc['$schema']='https://json-schema.org/draft/2020-12/schema';sc['components']={'schemas':SCHEMAS}
    dump('data/events/'+ev+'.v1.schema.json',sc)
dump('contracts/messaging-topology.json',dict(exchanges=[dict(name='depotflow.events',type='topic',durable=True),dict(name='depotflow.commands',type='topic',durable=True)],queues=[dict(name='q.'+s['id'],durable=True,type='quorum',bindings=[dict(exchange='depotflow.commands' if ev.endswith('requested') else 'depotflow.events',routing_key=ev+'.v1') for ev in s['consumes']],dead_letter_exchange='depotflow.dlx',dead_letter_routing_key='dlq.'+s['id'],prefetch=20,retry_delays_seconds=[1,2,4,8,16],jitter='full jitter',max_attempts=5) for s in SERVICES if s['consumes']],dead_letter=dict(exchange='depotflow.dlx',type='direct',queues=['dlq.'+s['id'] for s in SERVICES if s['consumes']],durable=True),publisher=dict(persistent=True,mandatory=True,confirms=True),consumer=dict(ack='after inbox+business+outbox transaction commits',dedupe='consumer+event_id',replay='preserve event_id and original metadata'),note='One node local not HA; 3node quorum lab only. Return/confirm does not mean consumer business processing completed. Retry worker publishes with confirms before ACK; never immediate requeue infinite loop.'))
write('contracts/README.md', '''# Contract conventions

OpenAPI3.1.1 JSON per service; AsyncAPI3.0 JSON per application; standalone JSON Schema2020-12 events in data/events. Design baseline only. Seven specs include all public/internal core operations. health/metrics infrastructure endpoints not business contracts. Placeholder .invalid DNS is deliberately non-routable. Gateway route mapping must avoid identical /v1 paths by prefix /api/{service}; frontend client generated accordingly.

Idempotency-Key required on business commands, length8..128; scope(org,subject,route,key), retention24h. Hash canonical JSON+route, durable response after commit; processing returns202 stable operation URL, same key/hash repeats, mismatch409. Retry after retention requires authoritative query first; retaining inbox longer than maximum DLQ replay horizon mandatory. Default inbox keep30d for history replay (N11 specifies minimum24h); older replay to rebuild projection uses new consumer namespace with no external side effects, not clearing existing inbox. Event archive retention30d lab, raw PII avoided.

If-Match quoted aggregate version on mutable updates/cancel/refund/physical forms. Missing428, stale412; intentional business conflict409. API status lookup returns authoritative state/version/updated_at. List cursor opaque signed org+filter+stable(created_at,id), limit default25 max100, no offset duplication during append. Authorization matrix PRD; list filters cannot widen own user/depot scope. Public tenant context derived from verified membership, never caller-supplied org. Internal X-Org/X-Subject are contextual claims and must match caller scope, token and original authorized subject. Browser cannot call internal routes.

Common error codes: invalid_auth, forbidden, not_found, idempotency_mismatch, inventory_conflict, hold_expired, cannot_cancel, handover_claimed, stale_version, validation_failed, precondition_required, rate_limited, dependency_unavailable, payment_unknown. Safe violations with paths; no stack traces/tokens. 429/503 Retry-After seconds, finite retry budget. Money EUR integer minor units, timestamps RFC3339 UTC; UUID identifiers.

Envelope mandatory event_id/type/schema_version/producer/org_id/aggregate_id/version/occurred_at/correlation/causation/data; traceparent optional but injected SDK required for instrumented flows. Commands data.command_id stable per business operation, never changed to defeat dedupe. Routing key type includes .v1. No implicit ordering across queues; fact handlers check prerequisites, project snapshots version-monotonic, late facts may trigger compensation. Async spec is not broker config; topology file defines queues/bindings/DLQ.

Backward compatibility: tolerant consumer ignores unknown optional fields, validates mandatory known ones; transport schemas remain closed in fixtures for drift detection. Introducing optional field requires old consumer proof, not simply saying JSON is extensible. Meaning/type/removal changes major v2; old/new coexist2releases, migration/runbook covers DLQ and event archive. All events from SERVICE registry must have schema, producer and consumer or documented external projection. Contract check helper verifies refs and schema shape; formal parser validation status documented in QA report, not inferred from JSON syntax.

Sandbox PSP adapter contract: authorize(key,amount,currency,expiry45d), query(key), capture(key,amount), void(key,remaining), refund(key,amount). Deterministic controls success/decline/processed-response-loss/delayed-webhook; signed callback uses timestamp and raw payload HMAC, test secrets generated in isolated lab. No real payment integration provided. Settlement remainder void emits payment.voided(kind=remainder); cancellation needs full void/no capture; Booking completes only after capture and remaining_authorization_minor0. Authorization validity shorter than max rental would require reauthorization saga, excluded by45d sandbox assumption.
''')
write('contracts/event-catalog.md','# Event catalog\n\nAll commands/facts version1. Org/correlation always envelope; the payload table is exact required schema in data/events.\n\n| Type | Owner | Consumers | Payload properties |\n|---|---|---|---|\n'+'\n'.join(f"|{ev}.v1|{next(s['id'] for s in SERVICES if ev in s['publishes'])}|{', '.join(s['id'] for s in SERVICES if ev in s['consumes']) or 'external lab projection'}|{', '.join(sc['properties'])}|" for ev,sc in EVENT_DATA.items()))
# Update service registry/passports with overrun consumers.
dump('architecture/services.json',SERVICES)
for owner in ['booking','fulfillment']:
    path=f'architecture/services/{owner}.md'
    old=DOCS[path];write(path,old+'\n\n## Overrun/damage projection\n\nAlso consumes asset.unavailable.v1; Booking raises affected booking incident, Fulfillment marks affected future job BLOCKED. Handover never trusts stale READY projection after authoritative check.')
write('architecture/services/inventory.md',DOCS['architecture/services/inventory.md']+'\n\n## Physical lifecycle\n\nConsumes fulfillment.handed-over to mark RENTED. Return-first events park until handover lookup and then finalize; a late handover fact never changes RETURNED asset back to RENTED. release_tombstones UNIQUE(org_id,booking_id) prevent delayed reserve resurrection. Handover-check validates active committed allocation and current physical readiness before claim; failure blocks physical action.')
write('architecture/services/catalog.md',DOCS['architecture/services/catalog.md']+'\n\n## Cache invalidation\n\nAlso consumes its own catalog.changed.v1 event to invalidate shared Redis model-list keys; handler does not publish another event. Cache misses/TTL60s handle lost or delayed invalidation, and quote always reads authoritative rate.')
write('product/business-processes.md',DOCS['product/business-processes.md']+'\n\n## Physical eligibility before claim\n\nFulfillment GET Inventory /internal/v1/bookings/{booking_id}/handover-check immediately before Booking claim. If not eligible/unavailable, stop; if check succeeds then claim serializes cancellation. Same job serialized at Fulfillment. Inventory consumes handed-over to mark RENTED; late return/handover uses job history not message arrival order. Operator verifies physical serial/condition before actual transfer; this physical check is required even if projection says READY. A failure after claim leaves manual review, not timed auto release.')
write('operations/network-security.md',DOCS['operations/network-security.md']+'\n\nAdditional allowed sync edge: Fulfillment → Inventory handover-check HTTPS, scope fulfillment and original operator/depot; failure blocks physical transfer.')
if __name__=='__main__': finish_registry(); print('HTTP operations:',len(OPS),'event schemas:',len(EVENT_DATA))
