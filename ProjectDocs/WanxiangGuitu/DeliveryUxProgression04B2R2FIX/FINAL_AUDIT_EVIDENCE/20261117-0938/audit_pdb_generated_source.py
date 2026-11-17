"""Follow-up to preserved first-pass diagnostic: distinguish generated source from drift."""
from pathlib import Path
import json,struct,hashlib,zlib
A=Path(__file__).resolve().parent;ns={'__file__':str(A/'read_pdb_checksums.py'),'__name__':'audit_parser'}
source=(A/'read_pdb_checksums.py').read_text(encoding='utf-8');exec(compile(source.split('out=A/')[0],str(A/'read_pdb_checksums.py'),'exec'),ns)
b=ns['b'];streams=ns['streams'];counts=ns['counts'];u32=ns['u32'];guid=ns['guid'];blob=ns['blob'];readidx=ns['readidx'];bw=ns['bw'];gw=ns['gw'];base=ns['base'];heaps=ns['heaps'];sw=4 if heaps&1 else 2
# Referenced type-system row counts are in #Pdb, not the debug table stream.
p=streams['#Pdb'][0]+24;mask=struct.unpack_from('<Q',b,p)[0];p+=8;allcounts=dict(counts)
for t in range(64):
 if mask>>t&1:allcounts[t]=u32(p);p+=4
ix=lambda t:4 if allcounts.get(t,0)>=65536 else 2
coded=4 if max(allcounts.values())>=2048 else 2
sizes={48:bw*2+gw*2,49:ix(48)+bw,50:ix(6)+ix(53)+ix(51)+ix(52)+8,51:4+sw,52:sw+bw,53:ix(53)+bw,54:2*ix(6),55:coded+gw+bw}
pos=base+24+4*len(counts);tableOffsets={}
for t,n in sorted(counts.items()):tableOffsets[t]=pos;pos+=sizes[t]*n
embedded={};meta=[]
for j in range(counts.get(55,0)):
 p=tableOffsets[55]+j*sizes[55];parent=readidx(p,coded);kind=guid(readidx(p+coded,gw));val=readidx(p+coded+gw,bw)
 if kind=='0e8a571b-6926-466e-b4ad-8ab04611f5fe' and parent&31==22:
  raw=blob(val);size=int.from_bytes(raw[:4],'little',signed=True);data=raw[4:] if size==0 else zlib.decompress(raw[4:],-15);assert size==0 or len(data)==size;embedded[parent>>5]=data
rows=ns['rows'];bad=[];generated=[]
for number,r in enumerate(rows,1):
 if not r['match']:
  assert 'Unity.SourceGenerators' in r['path'] and r['path'].endswith('AssemblyMonoScriptTypes.generated.cs'),'Unexpected actual source drift'
  data=embedded.get(number);entry={**r,'documentRow':number,'embeddedSourcePresent':data is not None}
  if data is not None:
   entry['embeddedChecksum']=hashlib.new(r['algorithm'],data).hexdigest();entry['embeddedMatchesCompiler']=entry['embeddedChecksum']==r['compilerChecksum'];out=A/'SOURCE_GENERATED'/Path(r['path']).name;out.parent.mkdir(exist_ok=True);assert not out.exists();out.write_bytes(data);entry['extractedPath']=out.as_posix()
  generated.append(entry)
  if data is None or not entry['embeddedMatchesCompiler']:bad.append(entry)
obj={**{k:v for k,v in ns['obj'].items() if k not in ['mismatches','result']},'projectSourcesMatched':sum(r['match'] for r in rows),'generatedSourceDocuments':generated,'unresolvedGenerated':bad,'firstPassDiagnostic':'COMPILER_PDB_SOURCE_CHECKSUMS.json intentionally preserved FAIL: it assumed every Document was a disk project file; this follow-up verifies generator embedded bytes, never alters original source/PDB/DLL.','result':'PASS' if not bad else 'CONDITIONAL_GENERATED_SOURCE_UNAVAILABLE'}
out=A/'PDB_SOURCE_AUDIT.json';assert not out.exists();out.write_text(json.dumps(obj,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in obj.items() if k!='documents'},indent=2))
