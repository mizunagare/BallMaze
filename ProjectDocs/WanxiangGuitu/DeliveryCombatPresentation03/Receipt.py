"""Read-only CP03 receipt classifier. Exit 0 PASS, 1 FAIL, 2 BLOCKED, 3 INCOMPLETE."""
import argparse, collections, csv, hashlib, json, math
from pathlib import Path

FROZEN_CONTRACTS = {
    "Editor": {
        "sha256": "6fb6024da5052be6604c23cb7be5e219860815278ebfae0bd0e86fc74e15a6f8",
        "layer": "controlled-editor",
        "scope": "Controlled public Strike/UseSkill and real projectiles; AI-disabled fixtures; not native/human/normal-AI victory",
        "sourceCommit": "42cfd3d8f3abd4861cd672dbb8f440fae48e4b65",
        "sourcePath": "ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03/Evidence/Final2/presentation.json"
    },
    "Runtime": {
        "sha256": "3f438369c590dfecfe27523dff3064ba9a2eba08caa89569425e5efd4418fb7a",
        "layer": "nondevelopment-acceptance-player; controlled public combat APIs, fixed fixtures; no synthetic input or injected Damage; Boot/Title and explicit controlled Continue from immutable synthetic checkpoint; NOT native click",
        "scope": "Controlled public Strike/UseSkill and real projectiles; AI-disabled fixtures; not native/human/normal-AI victory",
        "sourceCommit": "42cfd3d8f3abd4861cd672dbb8f440fae48e4b65",
        "sourcePath": "ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03/Evidence/Runtime2/presentation.json"
    }
}

class Invalid(ValueError): pass

def pairs(items):
    d={}
    for k,v in items:
        if k in d: raise Invalid("duplicate JSON key: "+k)
        d[k]=v
    return d

def load_bytes(raw):
    return json.loads(raw.decode("utf-8-sig"),object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(Invalid("nonfinite JSON: "+x)))

def load(path):
    return load_bytes(Path(path).read_bytes())

def rows_from(data):
    if not isinstance(data,dict): raise Invalid("receipt must be an object")
    for key in ("layer","scope"):
        if not isinstance(data.get(key),str) or not data[key].strip(): raise Invalid("missing/invalid "+key)
    rows=data.get("rows")
    if not isinstance(rows,list) or not rows: raise Invalid("rows must be a nonempty array")
    names=set()
    for row in rows:
        if not isinstance(row,dict): raise Invalid("row must be an object")
        name=row.get("name")
        if not isinstance(name,str) or not name.strip() or name!=name.strip(): raise Invalid("invalid assertion name")
        if name in names: raise Invalid("duplicate assertion: "+name)
        names.add(name)
        if row.get("status") not in ("PASS","FAIL","UNRESOLVED","NOT_RUN"): raise Invalid("unknown status: "+str(row.get("status")))
        if not isinstance(row.get("detail"),str): raise Invalid("invalid detail: "+name)
        for key in ("frame","time"):
            value=row.get(key)
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<0: raise Invalid("invalid "+key+": "+name)
        if not isinstance(row["frame"],int): raise Invalid("frame must be integral")
    return rows

def bind_contract(contract, profile, data, rows, info):
    # Trust comes from reviewed code constants, never from the supplied file or caller SHA.
    if not profile: raise Invalid("PROFILE_REQUIRED")
    if profile not in FROZEN_CONTRACTS: raise Invalid("UNKNOWN_PROFILE: "+str(profile))
    pin=FROZEN_CONTRACTS[profile]
    info.update(expectedSHA256=pin["sha256"],expectedLayer=pin["layer"],expectedScope=pin["scope"],sourceCommit=pin["sourceCommit"],sourcePath=pin["sourcePath"])
    if not contract: raise Invalid("CONTRACT_REQUIRED")
    raw=Path(contract).read_bytes();info["actualSHA256"]=hashlib.sha256(raw).hexdigest()
    if info["actualSHA256"]!=pin["sha256"]: raise Invalid("CONTRACT_SHA_MISMATCH")
    frozen=load_bytes(raw);required=rows_from(frozen)
    info.update(contractLayer=frozen["layer"],contractScope=frozen["scope"],requiredCount=len(required))
    for field in ("layer","scope"):
        if frozen[field]!=pin[field]: raise Invalid("CONTRACT_"+field.upper()+"_MISMATCH")
    info["contractVerified"]=True
    if data is None or not rows: raise Invalid("RECEIPT_INVALID_FOR_BINDING")
    info.update(receiptLayer=data.get("layer"),receiptScope=data.get("scope"))
    for field in ("layer","scope"):
        if data[field]!=pin[field]: raise Invalid("RECEIPT_"+field.upper()+"_MISMATCH")
    expected={r["name"] for r in required};actual={r["name"] for r in rows}
    if expected!=actual: raise Invalid("FROZEN_ASSERTION_SET_MISMATCH; missing="+repr(sorted(expected-actual))+"; extra="+repr(sorted(actual-expected)))
    info["status"]="PASS"


def evaluate(receipt, process_status="PASS", exit_code=0, timed_out=False, contract=None, external_failure=False, profile=None):
    errors=[];rows=[];counts={};data=None;receipt_sha=None
    binding=dict(status="INCOMPLETE",profile=profile,contractPath=str(contract) if contract else None,contractVerified=False,actualSHA256=None)
    process="PASS" if process_status=="PASS" and type(exit_code) is int and exit_code==0 and not timed_out else ("FAIL" if type(exit_code) is int and exit_code!=0 else "INCOMPLETE")
    try:
        raw=Path(receipt).read_bytes();receipt_sha=hashlib.sha256(raw).hexdigest();data=load_bytes(raw)
        rows=rows_from(data);counts=dict(collections.Counter(r["status"] for r in rows))
    except (OSError,ValueError,TypeError) as exc: errors.append(str(exc))
    try: bind_contract(contract,profile,data,rows,binding)
    except (OSError,ValueError,TypeError) as exc: errors.append(str(exc))
    integrity="PASS" if not errors and binding["status"]=="PASS" else "INCOMPLETE"
    assertions="FAIL" if counts.get("FAIL") else "UNRESOLVED" if counts.get("UNRESOLVED") else "NOT_RUN" if counts.get("NOT_RUN") else "PASS" if rows else "NOT_RUN"
    if external_failure: errors.append("Launcher reported an additional failure; inspect raw process/results receipts")
    if external_failure or process=="FAIL" or assertions=="FAIL": overall="FAIL"
    elif integrity!="PASS" or process!="PASS" or counts.get("NOT_RUN"): overall="INCOMPLETE"
    elif assertions=="UNRESOLVED": overall="BLOCKED"
    else: overall="PASS"
    return dict(process=dict(status=process,reportedStatus=process_status,exitCode=exit_code,timedOut=timed_out),
                integrity=integrity,assertionStatus=assertions if integrity=="PASS" else "INVALID",rawAssertionStatus=assertions,
                counts=counts,rows=rows,errors=errors,overallStatus=overall,binding=binding,
                exitCode={"PASS":0,"FAIL":1,"BLOCKED":2,"INCOMPLETE":3}[overall],
                contractSHA256=binding["actualSHA256"],receiptSHA256=receipt_sha)

def write(result, output):
    output=Path(output); output.mkdir(parents=True,exist_ok=False)
    (output/"acceptance.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    with (output/"assertions.csv").open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,["name","status","detail","frame","time"],extrasaction="ignore");w.writeheader();w.writerows(result["rows"])
    (output/"REPORT.md").write_text("# CP03 semantic acceptance\n\nProcess: "+result["process"]["status"]+
        "; assertions: "+result["assertionStatus"]+"; integrity: "+result["integrity"]+
        "; overall: **"+result["overallStatus"]+"**; classifier exit: "+str(result["exitCode"])+
        "\n\nFrozen binding: "+json.dumps(result["binding"],ensure_ascii=False)+"\n\n"+json.dumps(result["counts"])+"\n\n"+"\n".join(result["errors"])+
        "\n\nRaw receipts are not edited. Process PASS is not overall acceptance.\n",encoding="utf-8")

def main():
    a=argparse.ArgumentParser();a.add_argument("--receipt",required=True);a.add_argument("--output",required=True)
    a.add_argument("--contract",help="Required for acceptance; omission produces INCOMPLETE with a report");a.add_argument("--profile",help="Required trusted profile: Editor or Runtime");a.add_argument("--process-status",default="PASS");a.add_argument("--exit-code",type=int)
    a.add_argument("--external-failure",action="store_true");a.add_argument("--timed-out",action="store_true");o=a.parse_args()
    r=evaluate(o.receipt,o.process_status,o.exit_code,o.timed_out,o.contract,o.external_failure,o.profile);write(r,o.output)
    print(json.dumps({k:r[k] for k in ("process","assertionStatus","integrity","counts","binding","overallStatus","exitCode")}));return r["exitCode"]
if __name__=="__main__": raise SystemExit(main())
