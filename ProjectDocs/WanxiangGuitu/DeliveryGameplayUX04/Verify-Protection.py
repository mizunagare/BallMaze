"""Read-only Git history comparison and actual pre-run user hashes."""
import pathlib, subprocess, json, hashlib, sys
repo=pathlib.Path(sys.argv[1]); root=pathlib.Path(sys.argv[2])
start='eb11dd3d8350f7e7a89d94d2e45d4cfd203f53e9'
users=json.loads((root/'user-before.json').read_text(encoding='utf-8-sig'))
checks=[dict(path=x['Path'],before=x['Hash'].lower(),after=hashlib.sha256(pathlib.Path(x['Path']).read_bytes()).hexdigest()) for x in users]
paths=['ProjectDocs/WanxiangGuitu',':(exclude)ProjectDocs/WanxiangGuitu/DeliveryGameplayUX04',':(exclude)ProjectDocs/WanxiangGuitu/DEVELOPMENT_PLAN.md']
def changed(*revs):
    return subprocess.check_output(['git','-C',str(repo),'diff','--name-only',*revs,'--',*paths],text=True,encoding='utf-8').splitlines()
committed=changed(start,'HEAD');working=changed('HEAD')
result=dict(status='PASS' if not committed and not working and all(x['before']==x['after'] for x in checks) else 'FAIL',users=checks,historicalCommittedChanges=committed,historicalWorkingChanges=working,scope='Actual pre-run SHA256 for five user files; historical tracked deliveries compared through Git baseline and working diff. No claim of an unavailable full pre-run raw historical SHA256 snapshot.')
(root/'protection-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(result['status']);sys.exit(0 if result['status']=='PASS' else 1)
