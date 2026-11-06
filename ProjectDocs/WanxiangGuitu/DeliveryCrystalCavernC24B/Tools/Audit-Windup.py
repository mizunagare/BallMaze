"""Read-only audit of original windup samples. Never repairs source receipts."""
import csv, hashlib, json, pathlib, sys

VERSION = 'c24-windup-audit-1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read_json(p):
    def reject(value): raise ValueError('Non-finite JSON: '+value)
    return json.loads(p.read_text(encoding='utf-8-sig'), parse_constant=reject)

def main():
    source, output = map(pathlib.Path, sys.argv[1:3])
    output.mkdir(exist_ok=False)
    results=[]
    for name, mode in [('PlayerWindupA1','windup-a'),('PlayerWindupB1','windup-b')]:
        root=source/name
        files=['Player.command.json','Player.exit.json','process.json','entry-audit.jsonl',
               'cavern-test.txt','windup-summary.json','windup-timeline.tsv','windup-health.tsv','assertions.tsv']
        manifest=[dict(path=str(root/f),sha256=sha(root/f)) for f in files]
        command=read_json(root/'Player.command.json'); exit_receipt=read_json(root/'Player.exit.json')
        assert command['hostPid']==exit_receipt['hostPid'], 'PID mismatch'
        assert (root/'cavern-test.txt').read_text().strip()==mode, 'sample mode mismatch'
        assert str(root).lower().replace('\\','/') in ' '.join(command['arguments']).lower().replace('\\','/'), 'wrong run directory'
        try:
            read_json(root/'windup-summary.json')
            raise AssertionError('Malformed historical receipt was accepted')
        except (json.JSONDecodeError,ValueError) as error:
            negative=dict(status='PASS',result='REJECTED',reason=str(error))
        rows=list(csv.reader((root/'windup-timeline.tsv').open(),delimiter='\t'))
        assert rows and all(len(r)==8 for r in rows), 'invalid timeline'
        warnings=[r for r in rows if r[2]=='Warning']
        recovery=[r for r in rows if r[2]=='Recovery']
        locked=[r for r in warnings if float(r[4])<=.75]
        events=[json.loads(line) for line in (root/'entry-audit.jsonl').read_text(encoding='utf-8-sig').splitlines()]
        identities=[e for e in events if e.get('run')]
        result=dict(sample=name,mode=mode,inputFiles=manifest,command=command,exit=exit_receipt,
            entryIdentities=identities,originalJSONNegative=negative,
            observed=dict(firstWarning=warnings[0],firstObservedLockedDirection=locked[0],
                lockedDirections=sorted(set(r[5] for r in locked)),firstRecovery=recovery[0],lastFrame=rows[-1],
                observedHeroHPDecrease=float(rows[0][7])-float(rows[-1][7])),
            missing=['Explicit release event with attack identity/direction/damage',
                'Dedicated hero Damage event linking HP decrease to this release',
                'Explicit recovery-end event', 'Explicit transition event (B loop exits before writing frame)'],
            status='INCOMPLETE',scope='P1 Claw threshold only; no extrapolation')
        path=output/(name+'.json');path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        assert read_json(path)==result
        results.append(dict(sample=name,status=result['status'],outputSHA256=sha(path)))
    report=dict(toolVersion=VERSION,toolSHA256=sha(pathlib.Path(__file__)),samples=results,status='INCOMPLETE')
    (output/'audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return 3
if __name__=='__main__': sys.exit(main())
