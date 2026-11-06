import pathlib,json,csv,collections,hashlib
base=pathlib.Path(__file__).resolve().parents[1]; root=base/'Evidence'/'Runs'; records=[]
for d in sorted(root.iterdir()):
    if not d.is_dir() or not (d/'assertions.tsv').exists():continue
    raw=(d/'assertions.tsv').read_bytes();r=list(csv.reader(raw.decode('utf-8-sig').splitlines(),delimiter='\t'))
    counts=collections.Counter(x[1] for x in r if len(x)>1)
    process=json.loads((d/'process.json').read_text(encoding='utf-8-sig')) if (d/'process.json').exists() else None
    records.append(dict(run=d.name,layer='Editor' if d.name.startswith('Editor') else 'nondevelopment-test-Player',assertions=dict(counts),process=process,completed=(d/'complete.txt').exists(),sha256=hashlib.sha256(raw).hexdigest()))
totals={}
for layer in ['Editor','nondevelopment-test-Player']:
    c=collections.Counter()
    for r in records:
        if r['layer']==layer:c.update(r['assertions'])
    totals[layer]=dict(c)
out=dict(scope='All raw attempts including repeated setup assertions and historical failures. Not unique acceptance-case counts.',totals=totals,runs=records)
(base/'Evidence'/'run-summary.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(totals))
