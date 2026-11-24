"""Check links, structured reports, source identities and evidence hashes without Git writes."""
import pathlib,json,csv,hashlib,re,subprocess,collections
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['PLAYER_RUN_MATRIX.csv','FILES_CHANGED.tsv','BUILD_IDENTITY.tsv','PROTECTION_SHA256.tsv']:
    delimiter='\t' if name.endswith('.tsv') else ','
    with (D/name).open(encoding='utf-8',newline='') as f:rows=list(csv.reader(f,delimiter=delimiter))
    assert rows and all(len(x)==len(rows[0]) for x in rows),name
matrix=list(csv.DictReader((D/'PLAYER_RUN_MATRIX.csv').open(encoding='utf-8')))
has_release=(D/'RELEASE_RUNTIME/SUMMARY.json').exists()
assert len(matrix)==len({x['RunId'] for x in matrix})==(32 if has_release else 30)
assert collections.Counter(x['OriginalVerdict'] for x in matrix)=={'PASS':26 if has_release else 24,'FAIL':6}
assert collections.Counter(x['AcceptanceVerdict'] for x in matrix)=={'PASS':25 if has_release else 23,'NOT_ACCEPTED':7}
if has_release:
    original=list(csv.DictReader((D/'RELEASE_RUNTIME/ORIGINAL_30_RUN_MATRIX.csv').open(encoding='utf-8')))
    assert matrix[:30]==original,'Original 30 row identities or verdicts changed'
for row in matrix:
    p=D/row['Evidence'];m=json.loads((p/'run-manifest.json').read_text());res=json.loads((p/'result.json').read_text())
    assert row['RunId']==m['runId']==res['runId']
    assert int(row['PID'])==m['pid']==res['pid']
    assert row['OriginalVerdict']==res['verdict'] and int(row['ExitCode'])==res['exitCode']
    assert row['ProductDllSha256']==m['dllSha256'] and row['ExeSha256']==m['exeSha256']
for name in ['REPORT.md','ACCEPTANCE.md','TESTING.md','DATA_MAPPING.md','RISK_REGISTER.md']:
    for target in re.findall(r'\]\(([^)]+)\)',(D/name).read_text(encoding='utf-8')):
        if '://' not in target and not target.startswith('#'):assert (D/target.split('#')[0]).exists(),(name,target)
for rec in ['BUILD11','BUILD12_RELEASE']:
    text=(D/rec/'unity.log').read_text(encoding='utf-8',errors='replace')
    assert len(re.findall(r'^UX06_FIXTURE_PASS ',text,re.M))==14
    frozen=json.loads((D/rec/'FROZEN_INPUT_MANIFEST.json').read_text())
    assert len(frozen)==1516
    for row in frozen:assert sha(R/row['path'])==row['sha256'],row['path']
guids=collections.defaultdict(list)
for p in (R/'Assets').rglob('*.meta'):
    match=re.search(r'^guid: ([0-9a-f]{32})$',p.read_text(encoding='utf-8-sig',errors='strict'),re.M)
    if match:guids[match[1]].append(p.relative_to(R).as_posix())
changes=list(csv.DictReader((D/'FILES_CHANGED.tsv').open(encoding='utf-8'),delimiter='\t'))
for row in changes:
    p=R/row['Path'];assert sha(p)==row['Sha256'] and p.stat().st_size==int(row['Bytes'])
    if p.suffix=='.meta':
        match=re.search(r'^guid: ([0-9a-f]{32})$',p.read_text(),re.M)
        assert match and len(guids[match[1]])==1,row['Path']
assert (D/'SETTINGS_GATE/RECOVERY_PROPOSAL_6FILES.md').exists()
assert sha(D/'SETTINGS_GATE/RECOVERY_PROPOSAL_6FILES.md')=='404a4d13da5b7c796c871304d02aa6623ee8aa8808e4a2dd5efc29dfc1a342b6'
result={'status':'PASS','runRows':len(matrix),'originalVerdicts':dict(collections.Counter(x['OriginalVerdict'] for x in matrix)),'processAccepted':25 if has_release else 23,'notAccepted':7,'sourcePathRows':len(changes),'finalFixturesPerBuild':14,'finalFrozenInputsPerBuild':1516,'links':'PASS','csvColumnCounts':'PASS','newMetaGuids':'PASS','approvedRecoveryProposalSha256':'PASS'}
(D/'DELIVERY_CONSISTENCY.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
