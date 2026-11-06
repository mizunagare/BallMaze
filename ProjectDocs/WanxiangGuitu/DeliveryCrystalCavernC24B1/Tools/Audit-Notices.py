import json,pathlib,hashlib
root=pathlib.Path('I:/WGCombat/C24B1-1107-A'); out=root/'NoticeAudit1'
out.mkdir(exist_ok=False); rows=[]; inputs=[]
def read(p):
 b=p.read_bytes();inputs.append({'path':str(p),'sha256':hashlib.sha256(b).hexdigest()});return b.decode('utf-8-sig')
def load(p):return json.loads(read(p))
for name in ['b1-first-before-A1','b1-first-after-A1','RepeatPending1','RepeatClaimed1','RepeatSalvaged1']:
 d=root/name
 try:
  process=load(d/'process.json'); assert process['exitCode']==0 and not process['timedOut']
  events=[s.split('\t') for s in read(d/'notices.tsv').splitlines()]
  event={r[2]:r for r in events}; assert len(event)==len(events)
  for r in events:
   if r[4]=='True':assert '首奖可回营' not in r[-1] and '讨伐已保存' not in r[-1]
  c=event['confirmed'];dup=event['duplicate-retry'];assert c[4]=='False' and c[3:]==dup[3:]
  pre=load(d/'profile-before.json');post=load(d/'profile-after.json')
  death=load(d/'death-checkpoint.json');confirmed=load(d/'confirmed-checkpoint.json')
  assert death==confirmed, 'Full reward proof differs after retry'
  assert pre['profileId']==post['profileId']
  if name.startswith('Repeat'):
   assert pre['specialRewards']==post['specialRewards']
   assert pre['pending']==post['pending']
   assert '首奖' not in c[-1]
  else:assert '首奖可回营领取' in c[-1]
  rows.append(dict(run=name,status='PASS',profile=post['profileId'],fullRewardProofUnchanged=True,notice=c[-1]))
 except Exception as e:rows.append(dict(run=name,status='FAIL',error=str(e)))
(out/'inputs.json').write_text(json.dumps(inputs,indent=2),encoding='utf-8')
(out/'results.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
print([(x['run'],x['status'],x.get('error')) for x in rows])
raise SystemExit(any(x['status']!='PASS' for x in rows))
