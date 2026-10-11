"""Create self-contained ZIP and verify its CRC/files against source manifest."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and 'node_modules' not in p.parts and '__pycache__' not in p.parts and p.name!='manifest.json')
manifest={'note':'Hashes of actual source/artifact files; manifest itself excluded. Runtime implementation not included.','files':[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]}
(ROOT/'exports/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
archive=ROOT.parent/'DepotFlow-engineering-project.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files+[ROOT/'exports/manifest.json']:z.write(p,'engineering-project/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    bad=z.testzip()
    assert bad is None,bad
    for row in manifest['files']:
        assert hashlib.sha256(z.read('engineering-project/'+row['path'])).hexdigest()==row['sha256'],row['path']
sha=hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.zip.sha256').write_text(sha+'  '+archive.name+'\n',encoding='ascii')
print(json.dumps(dict(archive=str(archive),files=len(files)+1,bytes=archive.stat().st_size,sha256=sha,CRC='pass',manifest='pass'),ensure_ascii=False,indent=2))
