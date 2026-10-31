"""Read-only CP03 receipt classifier. Exit 0 PASS, 1 FAIL, 2 BLOCKED, 3 INCOMPLETE."""
import argparse, collections, csv, hashlib, json, math
from pathlib import Path

class Invalid(ValueError): pass

def pairs(items):
    d={}
    for k,v in items:
        if k in d: raise Invalid("duplicate JSON key: "+k)
        d[k]=v
    return d

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"),object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(Invalid("nonfinite JSON: "+x)))

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

def evaluate(receipt, process_status="PASS", exit_code=0, timed_out=False, contract=None, external_failure=False):
    errors=[]; rows=[]; counts={}; integrity="PASS"
    process="PASS" if process_status=="PASS" and type(exit_code) is int and exit_code==0 and not timed_out else ("FAIL" if type(exit_code) is int and exit_code!=0 else "INCOMPLETE")
    try:
        rows=rows_from(load(receipt)); counts=dict(collections.Counter(r["status"] for r in rows))
        if contract:
            required=rows_from(load(contract))
            expected={r["name"] for r in required}; actual={r["name"] for r in rows}
            if actual!=expected: raise Invalid("frozen assertion set mismatch; missing="+repr(sorted(expected-actual))+"; extra="+repr(sorted(actual-expected)))
    except (OSError,ValueError,TypeError) as exc:
        errors.append(str(exc)); integrity="INCOMPLETE"
    assertions="FAIL" if counts.get("FAIL") else "UNRESOLVED" if counts.get("UNRESOLVED") else "NOT_RUN" if counts.get("NOT_RUN") else "PASS" if rows else "NOT_RUN"
    if external_failure: errors.append("Launcher reported an additional failure; inspect raw process/results receipts")
    if external_failure or process=="FAIL" or assertions=="FAIL": overall="FAIL"
    elif integrity!="PASS" or process!="PASS" or counts.get("NOT_RUN"): overall="INCOMPLETE"
    elif assertions=="UNRESOLVED": overall="BLOCKED"
    else: overall="PASS"
    return dict(process=dict(status=process,reportedStatus=process_status,exitCode=exit_code,timedOut=timed_out),
                integrity=integrity,assertionStatus=assertions if integrity=="PASS" else "INVALID",
                counts=counts,rows=rows,errors=errors,overallStatus=overall,
                exitCode={"PASS":0,"FAIL":1,"BLOCKED":2,"INCOMPLETE":3}[overall],
                contractSHA256=hashlib.sha256(Path(contract).read_bytes()).hexdigest() if contract and Path(contract).is_file() else None,
                receiptSHA256=hashlib.sha256(Path(receipt).read_bytes()).hexdigest() if Path(receipt).is_file() else None)

def write(result, output):
    output=Path(output); output.mkdir(parents=True,exist_ok=False)
    (output/"acceptance.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    with (output/"assertions.csv").open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,["name","status","detail","frame","time"],extrasaction="ignore");w.writeheader();w.writerows(result["rows"])
    (output/"REPORT.md").write_text("# CP03 semantic acceptance\n\nProcess: "+result["process"]["status"]+
        "; assertions: "+result["assertionStatus"]+"; integrity: "+result["integrity"]+
        "; overall: **"+result["overallStatus"]+"**; classifier exit: "+str(result["exitCode"])+
        "\n\n"+json.dumps(result["counts"])+"\n\n"+"\n".join(result["errors"])+
        "\n\nRaw receipts are not edited. Process PASS is not overall acceptance.\n",encoding="utf-8")

def main():
    a=argparse.ArgumentParser();a.add_argument("--receipt",required=True);a.add_argument("--output",required=True)
    a.add_argument("--contract");a.add_argument("--process-status",default="PASS");a.add_argument("--exit-code",type=int)
    a.add_argument("--external-failure",action="store_true");a.add_argument("--timed-out",action="store_true");o=a.parse_args()
    r=evaluate(o.receipt,o.process_status,o.exit_code,o.timed_out,o.contract,o.external_failure);write(r,o.output)
    print(json.dumps({k:r[k] for k in ("process","assertionStatus","integrity","counts","overallStatus","exitCode")}));return r["exitCode"]
if __name__=="__main__": raise SystemExit(main())
