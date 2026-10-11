"""Structural/ref/link integrity checks of the assignment pack; not future business tests."""
import json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote,urlparse
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1];checks=[];errors=[]
def check(name,condition,detail=''):
    checks.append(dict(test=name,status='pass' if condition else 'failed',detail=detail))
    if not condition:errors.append(name+': '+detail)
def data(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
services=data('architecture/services.json');stories=data('requirements/functional.json');nfr=data('requirements/nonfunctional.json');ms=data('assignments/milestones.json');coverage=data('reviews/coverage.json');diagrams=data('architecture/diagrams/index.json');screens=data('design/screens.json');tracks=data('roadmaps/tracks.json')
check('seven independent owners',len(services)==7 and len({s['id'] for s in services})==7)
check('story registry',len(stories)==20);check('nfr registry',len(nfr)==12);check('18milestones',len(ms)==18);check('15roadmaps',len(tracks)==15);check('43rendered diagrams',len(diagrams)==43);check('22screen map',len(screens)==22)
for p in ROOT.rglob('*.json'):
    if 'node_modules'in p.parts:continue
    try:json.loads(p.read_text(encoding='utf-8-sig'))
    except Exception as e:check('JSON '+str(p.relative_to(ROOT)),False,str(e))
for c in coverage:
    check('coverage '+c['id'],bool(c['acceptance']) and (ROOT/c['spec']).exists() and (ROOT/c['assignment']).exists())
for s in services:
    for kind in ['openapi','asyncapi']:check(kind+' '+s['id'],(ROOT/f'contracts/{kind}/{s["id"]}.json').exists())
    for ev in s['publishes']+s['consumes']:check('event schema '+s['id']+'/'+ev,(ROOT/f'data/events/{ev}.v1.schema.json').exists())
for s in services:
    for ev in s['consumes']:check('producer for '+ev,len([x for x in services if ev in x['publishes']])==1)
def refs(o,top,name):
    if isinstance(o,dict):
        if '$ref'in o:
            ref=o['$ref'];target=top
            if ref.startswith('#/'):
                try:
                    for k in ref[2:].split('/'):target=target[k.replace('~1','/').replace('~0','~')]
                except Exception:check('ref '+name+' '+ref,False,'missing target')
        for v in o.values():refs(v,top,name)
    elif isinstance(o,list):
        for v in o:refs(v,top,name)
for p in list((ROOT/'contracts/openapi').glob('*.json'))+list((ROOT/'contracts/asyncapi').glob('*.json')):
    doc=json.loads(p.read_text(encoding='utf-8'));refs(doc,doc,p.name)
for d in diagrams:
    try:ET.parse(ROOT/d['path']);valid=True
    except Exception as e:valid=False
    check('SVG/source '+d['id'],valid and (ROOT/d['source']).exists() and (ROOT/d['doc']).exists())
required=['Title','Context','Learning Objectives','Prerequisites','Technical Requirements','Functional Requirements','Constraints','Expected Deliverables','Acceptance Criteria','Testing Scenarios','Failure Scenarios','Review','Definition of Done','Bonus']
for m in ms:
    text=(ROOT/f'assignments/{m["id"]}.md').read_text(encoding='utf-8');check('assignment sections '+m['id'],all(x in text for x in required))
    check('valid dependency '+m['id'],all(x in {n['id'] for n in ms} for x in m['depends']))
def visit(mid,ancestors):
    if mid in ancestors:return False
    return all(visit(d,ancestors|{mid}) for d in next(m for m in ms if m['id']==mid)['depends'])
check('acyclic milestone DAG',all(visit(m['id'],set()) for m in ms))
for s in screens:check('screen requirement '+s['id'],all(x in {v['id'] for v in stories} for x in s['requirements']))
for p in ROOT.rglob('*.md'):
    if 'node_modules' in p.parts:continue
    text=p.read_text(encoding='utf-8-sig')
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
        if target.startswith(('http:','https:','#')):continue
        q=target.split('#')[0]
        check('MD link '+p.relative_to(ROOT).as_posix()+' → '+target,(p.parent/unquote(q)).exists())
class Assets(HTMLParser):
    def __init__(self):super().__init__();self.targets=[]
    def handle_starttag(self,tag,attrs):
        for key,val in attrs:
            if key in ['src','href'] and val and not val.startswith(('http:','https:','#','data:')):self.targets.append(val)
for p in ROOT.rglob('*.html'):
    if 'node_modules'in p.parts:continue
    parser=Assets();parser.feed(p.read_text(encoding='utf-8'))
    for target in parser.targets:check('HTML asset '+p.relative_to(ROOT).as_posix()+' → '+target,(p.parent/unquote(target.split('#')[0])).exists())
payload=json.loads((ROOT/'atlas/content.json').read_text(encoding='utf-8'));check('offline doc index matches sources',all((ROOT/p).read_text(encoding='utf-8').strip()==t for p,t in payload['docs'].items()))
check('formal contract report passes',(ROOT/'reviews/evidence/contract-validation.json').exists() and data('reviews/evidence/contract-validation.json').get('passed',False))
check('browser report available',(ROOT/'reviews/evidence/browser-qa.json').exists())
report=dict(kind='assignment-pack-validation; not business acceptance',checks=checks,passed=not errors,errors=errors)
(ROOT/'reviews/evidence').mkdir(parents=True,exist_ok=True);(ROOT/'reviews/evidence/pack-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(checks=len(checks),passed=not errors,errors=errors),ensure_ascii=False,indent=2));sys.exit(0 if not errors else 1)

