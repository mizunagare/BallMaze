import pathlib,json,collections
d=pathlib.Path(__file__).resolve().parents[1];root=d/'Evidence/Runs';result={}
groups={
 'EditorCandidate':[p for p in root.glob('Editor-b1-*-A2')],
 'NonDevelopmentObservedCandidate':[root/x for x in ['b1-first-before-A1','b1-first-after-A1','b1-name-cavern-A1','b1-name-forest-A1','b1-ring-inner-A1','b1-ring-outer-A1','b1-ring-band-A1','b1-ring-safe-A1','RepeatPending1','PrepareClaimed1','RepeatClaimed1','RepeatSalvaged1']],
 'HistoricalReproduction':[root/'BeforeNotice1',root/'BeforeNames1Run'],
}
for layer,paths in groups.items():
 counts=collections.Counter();runs=[]
 for p in sorted(paths):
  process=json.loads((p/'process.json').read_text(encoding='utf-8-sig'))
  assert process['exitCode']==0 and process['exited'] and not process['timedOut']
  local=collections.Counter(line.split('\t')[1] for line in (p/'assertions.tsv').read_text(encoding='utf-8-sig').splitlines())
  counts.update(local);runs.append(dict(name=p.name,assertions=dict(local),process=process))
 result[layer]=dict(counts=dict(counts),runs=runs)
result['PureShipping']=json.loads((root/'PureTitle2/pure-runtime.json').read_text(encoding='utf-8-sig'))
result['N02EditorPOI']=json.loads((root/'ScoreComparison2/summary.json').read_text())
(d/'Evidence/layer-counts.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print({k:v.get('counts',v) if k!='PureShipping' else v['titleReady'] for k,v in result.items()})
