import pathlib,json,csv,hashlib
out=pathlib.Path(__file__).resolve().parent
j=json.loads((out/'PLAYER_REVIEW.json').read_text(encoding='utf-8'));dirs=json.loads((out/'DIRECTORY_HASHES.json').read_text(encoding='utf-8'))
assert j['summary']['reportedChecks']==99 and len(j['checks'])==99
assert all(c['observationMatched'] for c in j['checks'])
assert len(list(csv.DictReader((out/'CHECKS_99.csv').open(encoding='utf-8-sig'))))==99
assert all(r['identity_ok'] and r['build_ok'] and r['evidenceDir_ok'] and r['process_ok'] and not r['hash_bad'] for r in j['runs'])
assert all(x['ok'] for x in j['facts']) and j['restart']['ok']
assert len(j['lifecycle'])==15 and len(j['lifecycle'][0]['favAfter'])==1 and len(j['lifecycle'][-1]['favAfter'])==3
assert all(x['ok'] for x in j['native'])
for d in dirs:
 print(d['mode'],'files',len(d['files']),'tree',d['treeSHA256'],'sourceDiff',d['sourceDifferences'],'unlisted',d['unlisted'])
print('ALL AUDIT SELF-CHECKS PASS')
