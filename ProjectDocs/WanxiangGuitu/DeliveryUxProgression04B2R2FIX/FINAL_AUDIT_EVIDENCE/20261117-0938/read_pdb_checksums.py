"""Read existing Portable PDB and PE; NO compilation, execution, or modification."""
from pathlib import Path
import struct,hashlib,json,uuid
A=Path(__file__).resolve().parent;E=Path('Evidence/Runs04B2R2FIX/FINAL-A02/_product');pdb=E/'Assembly-CSharp.pdb';dll=E/'Assembly-CSharp.dll'
b=pdb.read_bytes();assert b[:4]==b'BSJB';u16=lambda o:struct.unpack_from('<H',b,o)[0];u32=lambda o:struct.unpack_from('<I',b,o)[0]
pos=(16+u32(12)+3)&~3;count=u16(pos+2);pos+=4;streams={}
for _ in range(count):
 off,size=u32(pos),u32(pos+4);end=b.index(0,pos+8);name=b[pos+8:end].decode();streams[name]=(off,size);pos=(end+4)&~3
base=streams['#~'][0];heaps=b[base+6];valid=struct.unpack_from('<Q',b,base+8)[0];assert valid&((1<<48)-1)==0,'Unexpected non-debug table before Document'
pos=base+24;counts={}
for i in range(64):
 if valid>>i&1:counts[i]=u32(pos);pos+=4
assert 48 in counts;bw=4 if heaps&4 else 2;gw=4 if heaps&2 else 2
readidx=lambda o,w:int.from_bytes(b[o:o+w],'little')
def compressed(o):
 z=b[o]
 if z<128:return z,o+1
 if z<192:return ((z&63)<<8)|b[o+1],o+2
 return ((z&31)<<24)|(b[o+1]<<16)|(b[o+2]<<8)|b[o+3],o+4

def blob(i):
 n,o=compressed(streams['#Blob'][0]+i);return b[o:o+n]
def guid(i):
 o=streams['#GUID'][0]+(i-1)*16;return str(uuid.UUID(bytes_le=b[o:o+16]))
def docname(i):
 raw=blob(i);sep=chr(raw[0]);parts=[];j=1
 while j<len(raw):
  z=raw[j]
  if z<128:v=z;j+=1
  elif z<192:v=((z&63)<<8)|raw[j+1];j+=2
  else:v=((z&31)<<24)|(raw[j+1]<<16)|(raw[j+2]<<8)|raw[j+3];j+=4
  parts.append(blob(v).decode('utf-8'))
 return sep.join(parts)
rows=[]
for _ in range(counts[48]):
 name=docname(readidx(pos,bw));pos+=bw;alg=guid(readidx(pos,gw));pos+=gw;checksum=blob(readidx(pos,bw)).hex();pos+=bw;pos+=gw
 algo={'8829d00f-11b8-4213-878b-770e8597ac16':'sha256','ff1816ec-aa5e-4d10-87f7-6f4963833460':'sha1'}.get(alg);p=Path(name);actual=hashlib.new(algo,p.read_bytes()).hexdigest() if algo and p.is_file() else None
 rows.append({'path':name,'algorithm':algo,'compilerChecksum':checksum,'currentChecksum':actual,'match':actual==checksum})
pe=dll.read_bytes();U16=lambda o:struct.unpack_from('<H',pe,o)[0];U32=lambda o:struct.unpack_from('<I',pe,o)[0];h=U32(0x3c);assert pe[h:h+4]==b'PE\0\0';opt=h+24;data=opt+(112 if U16(opt)==0x20b else 96);drva,dsize=U32(data+48),U32(data+52);sec=opt+U16(h+20)
def fileoff(rva):
 for k in range(U16(h+6)):
  t=sec+40*k;va=U32(t+12)
  if va<=rva<va+max(U32(t+8),U32(t+16)):return U32(t+20)+rva-va
 raise ValueError('RVA unmapped')
debug=fileoff(drva);bindings=[];pdbid=b[streams['#Pdb'][0]:streams['#Pdb'][0]+20]
for t in range(debug,debug+dsize,28):
 typ,sz,ptr=U32(t+12),U32(t+16),U32(t+24);raw=pe[ptr:ptr+sz]
 if typ==2:
  assert raw[:4]==b'RSDS';bindings.append({'type':'CodeView','guidMatches':raw[4:20]==pdbid[:16],'stampMatches':pe[t+4:t+8]==pdbid[16:20],'embeddedPdbPath':raw[24:].split(b'\0')[0].decode(errors='replace')})
assert bindings and all(x['guidMatches'] and x['stampMatches'] for x in bindings);bad=[x for x in rows if not x['match']]
obj={'scope':'Compiler-recorded Portable PDB Document checksums, independently parsed without a build or Player. PE CodeView GUID+stamp bound to existing PDB ID. This is new audit evidence, not a retroactive build receipt.','productDLLSHA256':hashlib.sha256(pe).hexdigest(),'pdbSHA256':hashlib.sha256(b).hexdigest(),'pePdbBinding':bindings,'documentCount':len(rows),'mismatches':bad,'documents':rows,'result':'PASS' if not bad else 'FAIL'}
out=A/'COMPILER_PDB_SOURCE_CHECKSUMS.json';assert not out.exists();out.write_text(json.dumps(obj,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in obj.items() if k!='documents'},indent=2));assert not bad
