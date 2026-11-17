"""Freeze literal allowlist only. NEVER invokes git add or mutates existing payload."""
from pathlib import Path
import json,csv,hashlib,subprocess
R=Path.cwd(); D=Path('ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1'); A=D/'FINAL_AUDIT_EVIDENCE/20261116-1343'; H=json.loads((A/'history/HISTORY_PATH_HASH_MISSING.json').read_text(encoding='utf-8')); entries={}
def norm(p):return str(p).replace(chr(92),'/')
def add(p,category,reason):
    p=norm(p)
    e=entries.setdefault(p,{'path':p,'categories':set(),'reasons':set()});e['categories'].add(category);e['reasons'].add(reason)
def paths(key):
    for x in H[key]:yield x if isinstance(x,str) else x['path']
new=['B2AttackModel.cs','B2InventoryQuery.cs','B2Collection.cs'];mod=['AdventureLoadout.cs','CatInventoryPresenter.cs','ContainerInventoryView.cs','CampRuntime.cs','CampInventoryView.cs']
for n in new:add('Assets/CombatPrototype/'+n,'A','B2新增产品源')
for n in mod:add('Assets/CombatPrototype/'+n,'B','B2原有tracked修改，最终内容含R1')
temporal=json.loads((A/'protection/SOURCE_TEMPORAL_CLASSIFICATION.json').read_text(encoding='utf-8'))
for e in temporal:
    if e['changed_B2_to_R1']:add(e['path'],'C','相对09:57原B2八源快照的R1修改；C与A/B可重叠')
for n in new:add('Assets/CombatPrototype/'+n+'.meta','D','三个新增源对应唯一meta')
for p in paths('candidateFormalFiles_NOT_FINAL_WHITELIST'):add(p,'E','已逐项核验正式文档/工具/基线与设计输入；设计输入不授权新增功能')
for p in paths('candidateEvidenceFiles_NOT_FINAL_WHITELIST'):
    if p.endswith('.pdb') or p.endswith('.ref.dll'):continue
    p=norm(p); history=('/A01/' in p or '/A02/' in p or 'manual-A02' in p or ('Evidence/Runs04B2/UX04-B2-' in p and '-FINAL/' not in p))
    add(p,'G' if history else 'F','保留相关历史原件' if history else '正式Player/构建身份原件')
for p in paths('mustPreserveFailureFiles'):add(p,'G','最低不可丢弃失败原件')
for p in (D/'EVIDENCE').rglob('*'):
    if p.is_file() and p.name!='INDEX.json' and any(x in ('recompute-A01','recompute-A01-schema2') for x in p.parts):add(p,'G','失败复算明细原件，不以最终PASS覆盖')
# All new authoritative audit attachments; omit throwaway console-format discovery dumps.
for p in A.rglob('*'):
    if p.is_file() and p.name not in ('structure.txt','structure_utf8.txt','WHITELIST_SUMMARY.json','SUBMIT_WHITELIST.csv','AUDIT_INDEX.json') and not p.suffix=='.pyc':add(p,'E','FINAL只读审计附件')
for p in [D/'FINAL_AUDIT.md',D/'SUBMIT_WHITELIST.txt',A/'SUBMIT_WHITELIST.csv',A/'AUDIT_INDEX.json',A/'WHITELIST_SUMMARY.json']:add(p,'E','本轮最终报告与冻结元清单')
# Classify declared old failed recompute reports as both formal and required history.
for p,e in entries.items():
    if 'recompute-A01' in p:e['categories'].add('G')
for p in entries:
    assert not p.startswith(('Builds/','Library/','Packages/','ProjectSettings/','UserSettings/','Logs/')) and p!='Assets/Resources.meta',p
    assert p not in ['Assets/Settings/PC_RPAsset.asset'],p
    assert not ('/_roots/' in p),p
    if p.startswith('Assets/'):assert p in {'Assets/CombatPrototype/'+n for n in new+mod+ [n+'.meta' for n in new]},p
# No mutations of Git; only query ignore metadata. Nonzero 1 means none ignored.
proc=subprocess.run(['git','check-ignore','-v','--stdin'],input=chr(10).join(sorted(entries))+chr(10),capture_output=True,text=True)
assert proc.returncode in (0,1),(proc.returncode,proc.stderr)
ignore_lines=proc.stdout.splitlines(); ignored={line.split('	',1)[1] for line in ignore_lines if '	' in line}
text=D/'SUBMIT_WHITELIST.txt'; ledger=A/'SUBMIT_WHITELIST.csv'; summary=A/'WHITELIST_SUMMARY.json'; idx=A/'AUDIT_INDEX.json'
assert not any(p.exists() for p in [text,ledger,summary,idx]),'Refuse replacing frozen artifacts'
header="""# UX-04-B2-R1-FINAL 提交白名单（冻结候选，不是暂存/提交授权）
# A新增源 B原B2修改源 C相对原B2快照的R1修改 D新增meta E文档/工具/审计 F正式Player/构建 G必须历史原件
# C是重叠标签，同一路径只列一次；只允许未来负责人明确批准后逐条 git add --sparse -f -- <单一路径>，本轮未执行。
# 排除Builds/Library/Assets/Resources.meta/四个Unity设置文件/ProjectSettings/Packages/场景Prefab/运行roots/临时日志/无关历史Evidence及用户改动。
# PreImplementationAudit作为历史设计输入归档，不代表执行未批准设计；本新清单代替旧B2候选分类，但不改旧清单原件。
# 本清单不弥补缺失driver二进制；A03与B2最终driver仅在Builds live，不自动复制或纳入。

"""
lines=[]
for p,e in sorted(entries.items()):lines.extend(['# '+','.join(sorted(e['categories']))+' | '+'; '.join(sorted(e['reasons'])),p])
text.write_text(header+chr(10).join(lines)+chr(10),encoding='utf-8')
selfmeta={norm(ledger),norm(idx),norm(summary)}; rows=[]
for p,e in sorted(entries.items()):
    path=Path(p); assert path.is_file() or p in selfmeta,p
    # Self-referential meta artifacts are named but not falsely claimed to self-hash.
    digest='SELF_REFERENTIAL_META' if p in selfmeta else hashlib.file_digest(path.open('rb'),'sha256').hexdigest(); size='' if p in selfmeta else path.stat().st_size
    rows.append({'path':p,'categories':','.join(sorted(e['categories'])),'sha256':digest,'bytes':size,'ignoredNow':p in ignored,'futureStaging':'git add --sparse -f -- '+json.dumps(p,ensure_ascii=False),'reason':'; '.join(sorted(e['reasons']))})
with ledger.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
bycategory={c:sum(c in e['categories'] for e in entries.values()) for c in 'ABCDEFG'}
summary.write_text(json.dumps({'candidateUniquePaths':len(entries),'overlappingCategoryCounts':bycategory,'ignoreExitCode':proc.returncode,'ignoredMatches':ignore_lines,'exclusions':['Builds','Library','Assets/Resources.meta','Assets/Settings/PC_RPAsset.asset','ProjectSettings','Packages','UserSettings','scenes/prefabs','_roots','unrelated history'],'authorization':'none; frozen candidate only','metaHashPolicy':'CSV/summary/index cannot hash themselves; AUDIT_INDEX hashes CSV and summary, not itself'},ensure_ascii=False,indent=2),encoding='utf-8')
# Includes existing payload + all final audit files, without an impossible index self-hash.
artifacts=[{'path':norm(p),'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest(),'bytes':p.stat().st_size} for p in sorted(A.rglob('*')) if p.is_file() and p!=idx and norm(p) in entries]
idx.write_text(json.dumps({'scope':'FINAL audit attachments only; original INDEX files untouched','artifacts':artifacts,'report':{'path':norm(D/'FINAL_AUDIT.md'),'sha256':hashlib.file_digest((D/'FINAL_AUDIT.md').open('rb'),'sha256').hexdigest()},'literalAllowlist':{'path':norm(text),'sha256':hashlib.file_digest(text.open('rb'),'sha256').hexdigest()},'payloadCount':len(entries)},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'candidateUniquePaths':len(entries),'categories':bycategory,'allLiteralFiles':True,'noGitMutation':True},indent=2))
