import sys,re,json
from pathlib import Path
sys.path.insert(0,'I:/WGCombat/CP04BR2-1102-A/PythonLib')
import capstone,pefile
p=Path('C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.dll');pe=pefile.PE(str(p),fast_load=True);base=pe.OPTIONAL_HEADER.ImageBase
symbols={}
for s in Path('I:/WGCombat/CP04BR2-1102-A/native-symbols.txt').read_text().splitlines():
 m=re.match(r'([0-9a-f]+) size=\d+ (.*)',s)
 if m:symbols[int(m[1],16)]=m[2]
out=[];cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
for name,start,length in [('BaseConnectSettingsGetEnabled',0x182711c00,0x10),('CrashReportingGetEnabled',0x182717c80,0xc0),('InitializeSettings',0x1827207d0,0x400)]:
 rows=[]
 for i in cs.disasm(pe.get_data(start-base,length),start):
  rows.append({'va':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str,'symbol':symbols.get(int(i.op_str,16),'') if i.mnemonic in ['call','jmp'] and re.fullmatch('0x[0-9a-f]+',i.op_str) else ''})
 out.append({'name':name,'rangeStart':hex(start),'length':length,'instructions':rows})
Path('I:/WGCombat/CP04BR2-1102-A/native-service-disassembly.json').write_text(json.dumps(out,indent=2))
for f in out:
 print(f['name']);print('\n'.join(f"{x['va']} {x['mnemonic']} {x['operands']} {x['symbol']}" for x in f['instructions']))


