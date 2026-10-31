"""Read-only CP03 receipt classifier. Exit 0 PASS, 1 FAIL, 2 BLOCKED, 3 INCOMPLETE."""
import argparse, collections, csv, hashlib, json, math, re
from pathlib import Path
from datetime import datetime

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


PROCESS_SPECS = {
    "Editor": {"name": "CP03Editor.Run", "scope": "controlled-editor", "exe": "unity.exe"},
    "Runtime": {"name": "CP03Runtime", "scope": "nondevelopment-acceptance-player-controlled-combat-API", "exe": "wanxiangguitu.exe"}
}
PROCESS_STATUSES = ("PASS", "FAIL", "NOT_RUN")

def code_valid(value):
    return type(value) is int and -(2**31)<=value<=2**32-1

def utc_time(value):
    if not isinstance(value,str): raise Invalid("INVALID_PROCESS_TIMESTAMP")
    try: result=datetime.fromisoformat(value.replace("Z","+00:00"))
    except ValueError: raise Invalid("INVALID_PROCESS_TIMESTAMP")
    if result.tzinfo is None or result.utcoffset() is None: raise Invalid("PROCESS_TIMESTAMP_TIMEZONE_REQUIRED")
    return result

def absolute_source_path(value,reason):
    if not isinstance(value,str) or not value or not Path(value).is_absolute(): raise Invalid(reason)
    return Path(value).resolve()

def associate_process_sources(root,prefix,row,native,snapshot_sha,command_receipt,process_origin,desktop_receipt,info,start,end,observed):
    required=(("commandReceipt",command_receipt,Path(str(prefix)+".command.json")),
              ("originReceipt",process_origin,root/"process-origin.json"),
              ("desktopReceipt",desktop_receipt,Path(str(prefix)+".desktop-process.json")))
    data={}
    for label,given,expected in required:
        if not given: raise Invalid(label.upper()+"_REQUIRED")
        path=Path(given).resolve()
        if path!=expected: raise Invalid(label.upper()+"_RUN_PATH_MISMATCH")
        raw=path.read_bytes();info[label]=dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest())
        data[label]=load_bytes(raw)
        if not isinstance(data[label],dict): raise Invalid(label.upper()+"_INVALID_OBJECT")
    command=data["commandReceipt"];origin=data["originReceipt"];desktop=data["desktopReceipt"]
    if type(command.get("hostPid")) is not int or command["hostPid"]<=0: raise Invalid("INVALID_COMMAND_HOST_PID")
    if command["hostPid"]!=native["hostPid"]: raise Invalid("NATIVE_COMMAND_HOSTPID_MISMATCH")
    exe=absolute_source_path(command.get("exe"),"INVALID_COMMAND_EXE_PATH")
    runner_exe=absolute_source_path(row["command"][0],"INVALID_RUNNER_EXE_PATH")
    if exe!=runner_exe: raise Invalid("COMMAND_RUNNER_EXE_MISMATCH")
    args=command.get("arguments")
    if not isinstance(args,list) or any(not isinstance(x,str) for x in args): raise Invalid("INVALID_COMMAND_ARGUMENTS")
    if args!=row["command"][1:]: raise Invalid("COMMAND_RUNNER_ARGUMENTS_MISMATCH")
    if absolute_source_path(origin.get("source"),"INVALID_ORIGIN_SOURCE_PATH")!=root/"results.json": raise Invalid("ORIGIN_SOURCE_PATH_MISMATCH")
    if absolute_source_path(origin.get("snapshot"),"INVALID_ORIGIN_SNAPSHOT_PATH")!=root/"process-results.json": raise Invalid("ORIGIN_SNAPSHOT_PATH_MISMATCH")
    if not (root/"results.json").is_file(): raise Invalid("ORIGIN_SOURCE_FILE_MISSING")
    for key in ("sourceSHA256AtSnapshot","snapshotSHA256"):
        value=origin.get(key)
        if not isinstance(value,str) or re.fullmatch("[0-9a-fA-F]{64}",value) is None: raise Invalid("INVALID_ORIGIN_SHA_"+key)
        if value.lower()!=snapshot_sha: raise Invalid("ORIGIN_SNAPSHOT_SHA_MISMATCH_"+key)
    if absolute_source_path(desktop.get("exe"),"INVALID_DESKTOP_EXE_PATH")!=exe: raise Invalid("DESKTOP_COMMAND_EXE_MISMATCH")
    if type(desktop.get("pid")) is not int or desktop["pid"]<=0: raise Invalid("INVALID_DESKTOP_PID")
    launched=utc_time(command.get("startUtc"));created=utc_time(desktop.get("utc"));captured=utc_time(origin.get("utc"))
    if not start<=launched<=created<=observed<=end: raise Invalid("COMMAND_DESKTOP_TIME_SEQUENCE_MISMATCH")
    if captured<end: raise Invalid("ORIGIN_CAPTURE_BEFORE_STAGE_END")
    info.update(associationStatus="PASS",nativeHostPid=native["hostPid"],commandHostPid=command["hostPid"],desktopPid=desktop["pid"],actualExecutable=str(exe),arguments=args,originSource=str(root/"results.json"),originSnapshot=str(root/"process-results.json"))


def process_from_files(receipt,profile,process_receipt,exit_receipt,process_status,exit_code,timed_out,command_receipt,process_origin,desktop_receipt):
    result=dict(status="INCOMPLETE",evidenceStatus="INCOMPLETE",reportedStatus=None,exitCode=None,timedOut=None,
                source=dict(kind="associated-runner-native-command-origin-desktop",associationStatus="INCOMPLETE",runnerReceipt=None,exitReceipt=None,commandReceipt=None,originReceipt=None,desktopReceipt=None),
                claims=dict(status=process_status,exitCode=exit_code,timedOut=timed_out),errors=[])
    try:
        if process_status is not None and (not isinstance(process_status,str) or process_status not in PROCESS_STATUSES): raise Invalid("INVALID_PROCESS_STATUS_CLAIM")
        if exit_code is not None and not code_valid(exit_code): raise Invalid("INVALID_EXIT_CODE_CLAIM")
        if timed_out is not None and type(timed_out) is not bool: raise Invalid("INVALID_TIMED_OUT_CLAIM")
        if not process_receipt: raise Invalid("PROCESS_RECEIPT_REQUIRED")
        if not exit_receipt: raise Invalid("EXIT_RECEIPT_REQUIRED")
        if profile not in PROCESS_SPECS: raise Invalid("PROCESS_PROFILE_REQUIRED_OR_UNKNOWN")
        spec=PROCESS_SPECS[profile];rp=Path(process_receipt).resolve();ep=Path(exit_receipt).resolve()
        if rp.name!="process-results.json": raise Invalid("UNRECOGNIZED_RUNNER_RECEIPT_NAME")
        if rp.parent!=Path(receipt).resolve().parent: raise Invalid("PROCESS_RECEIPT_RUN_ROOT_MISMATCH")
        prefix=rp.parent/spec["name"]
        if ep!=Path(str(prefix)+".exit.json"): raise Invalid("PROCESS_EXIT_PAIR_MISMATCH")
        raw=rp.read_bytes();result["source"]["runnerReceipt"]=dict(path=str(rp),sha256=hashlib.sha256(raw).hexdigest())
        data=load_bytes(raw);items=data if isinstance(data,list) else [data]
        if not items or any(not isinstance(x,dict) for x in items): raise Invalid("INVALID_RUNNER_RECEIPT")
        target=[x for x in items if x.get("name")==spec["name"]]
        if len(target)!=1: raise Invalid("PROCESS_STAGE_MISSING_OR_DUPLICATE")
        row=target[0]
        result.update(reportedStatus=row.get("status"),exitCode=row.get("exitCode"),timedOut=row.get("timedOut"))
        if not isinstance(row.get("status"),str) or row["status"] not in PROCESS_STATUSES: raise Invalid("INVALID_OR_MISSING_PROCESS_STATUS")
        if "exitCode" not in row or not code_valid(row["exitCode"]): raise Invalid("INVALID_OR_MISSING_EXIT_CODE")
        if "timedOut" not in row or type(row["timedOut"]) is not bool: raise Invalid("INVALID_OR_MISSING_TIMED_OUT")
        if row.get("scope")!=spec["scope"]: raise Invalid("PROCESS_SCOPE_MISMATCH")
        if not isinstance(row.get("log"),str) or Path(row["log"]).resolve()!=prefix: raise Invalid("PROCESS_LOG_PREFIX_MISMATCH")
        command=row.get("command")
        if not isinstance(command,list) or not command or any(not isinstance(x,str) for x in command) or Path(command[0]).name.lower()!=spec["exe"]: raise Invalid("PROCESS_EXECUTABLE_MISMATCH")
        start=utc_time(row.get("startUtc"));end=utc_time(row.get("endUtc"))
        if start>end: raise Invalid("PROCESS_TIME_ORDER_INVALID")
        if row["timedOut"]: raise Invalid("PROCESS_TIMED_OUT_NOT_ACCEPTABLE")
        if row["status"]=="NOT_RUN": raise Invalid("PROCESS_NOT_STARTED")
        if row["status"]=="PASS" and row["exitCode"]!=0 or row["status"]=="FAIL" and row["exitCode"]==0: raise Invalid("PROCESS_STATUS_EXIT_CONTRADICTION")
        raw=ep.read_bytes();result["source"]["exitReceipt"]=dict(path=str(ep),sha256=hashlib.sha256(raw).hexdigest())
        native=load_bytes(raw)
        if not isinstance(native,dict) or not code_valid(native.get("exitCode")): raise Invalid("INVALID_NATIVE_EXIT_CODE")
        if type(native.get("forcedTermination")) is not bool or native["forcedTermination"]: raise Invalid("NATIVE_FORCED_OR_UNCONFIRMED_TERMINATION")
        if type(native.get("hostPid")) is not int or native["hostPid"]<=0: raise Invalid("INVALID_NATIVE_HOST_PID")
        observed=utc_time(native.get("exitObservedUtc"))
        if not start<=observed<=end: raise Invalid("NATIVE_EXIT_OUTSIDE_STAGE_INTERVAL")
        if native["exitCode"]!=row["exitCode"]: raise Invalid("NATIVE_RUNNER_EXIT_MISMATCH")
        if process_status is not None and process_status!=row["status"]: raise Invalid("PROCESS_STATUS_CLAIM_MISMATCH")
        if exit_code is not None and exit_code!=row["exitCode"]: raise Invalid("EXIT_CODE_CLAIM_MISMATCH")
        if timed_out is not None and timed_out!=row["timedOut"]: raise Invalid("TIMED_OUT_CLAIM_MISMATCH")
        associate_process_sources(rp.parent,prefix,row,native,result["source"]["runnerReceipt"]["sha256"],command_receipt,process_origin,desktop_receipt,result["source"],start,end,observed)
        result["source"].update(stage=spec["name"],scope=row["scope"],logPrefix=str(prefix),startUtc=row["startUtc"],endUtc=row["endUtc"],nativeExitObservedUtc=native["exitObservedUtc"],nativeHostPid=native["hostPid"],forcedTermination=native["forcedTermination"])
        result.update(status=row["status"],evidenceStatus="PASS")
    except (OSError,ValueError,TypeError) as exc: result["errors"].append(str(exc))
    return result


def evaluate(receipt, process_status=None, exit_code=None, timed_out=None, contract=None, external_failure=False, profile=None, process_receipt=None, exit_receipt=None, command_receipt=None, process_origin=None, desktop_receipt=None):
    errors=[];rows=[];counts={};data=None;receipt_sha=None
    binding=dict(status="INCOMPLETE",profile=profile,contractPath=str(contract) if contract else None,contractVerified=False,actualSHA256=None)
    process=process_from_files(receipt,profile,process_receipt,exit_receipt,process_status,exit_code,timed_out,command_receipt,process_origin,desktop_receipt)
    errors.extend(process["errors"])
    try:
        raw=Path(receipt).read_bytes();receipt_sha=hashlib.sha256(raw).hexdigest();data=load_bytes(raw)
        rows=rows_from(data);counts=dict(collections.Counter(r["status"] for r in rows))
    except (OSError,ValueError,TypeError) as exc: errors.append(str(exc))
    try: bind_contract(contract,profile,data,rows,binding)
    except (OSError,ValueError,TypeError) as exc: errors.append(str(exc))
    integrity="PASS" if not errors and binding["status"]=="PASS" else "INCOMPLETE"
    assertions="FAIL" if counts.get("FAIL") else "UNRESOLVED" if counts.get("UNRESOLVED") else "NOT_RUN" if counts.get("NOT_RUN") else "PASS" if rows else "NOT_RUN"
    if external_failure: errors.append("Launcher reported an additional failure; inspect raw process/results receipts")
    if process["evidenceStatus"]!="PASS": overall="INCOMPLETE"
    elif external_failure or process["status"]=="FAIL" or assertions=="FAIL": overall="FAIL"
    elif integrity!="PASS" or process["status"]!="PASS" or counts.get("NOT_RUN"): overall="INCOMPLETE"
    elif assertions=="UNRESOLVED": overall="BLOCKED"
    else: overall="PASS"
    return dict(process=process,
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
        "; process evidence: "+json.dumps(result["process"],ensure_ascii=False)+"; assertions: "+result["assertionStatus"]+"; integrity: "+result["integrity"]+
        "; overall: **"+result["overallStatus"]+"**; classifier exit: "+str(result["exitCode"])+
        "\n\nFrozen binding: "+json.dumps(result["binding"],ensure_ascii=False)+"\n\n"+json.dumps(result["counts"])+"\n\n"+"\n".join(result["errors"])+
        "\n\nRaw receipts are not edited. Process PASS is not overall acceptance.\n",encoding="utf-8")

def main():
    a=argparse.ArgumentParser();a.add_argument("--receipt",required=True);a.add_argument("--output",required=True)
    a.add_argument("--contract",help="Required for acceptance; omission produces INCOMPLETE with a report");a.add_argument("--profile",help="Required trusted profile: Editor or Runtime");a.add_argument("--process-status",help="Optional consistency claim, never proof");a.add_argument("--exit-code",help="Optional consistency claim, never proof");a.add_argument("--process-receipt",help="Required actual runner results snapshot");a.add_argument("--exit-receipt",help="Required matching NativeProbe exit receipt");a.add_argument("--command-receipt",help="Required same-run command.json");a.add_argument("--process-origin",help="Required same-run snapshot origin");a.add_argument("--desktop-receipt",help="Required same-run desktop process receipt")
    a.add_argument("--external-failure",action="store_true");t=a.add_mutually_exclusive_group();t.add_argument("--timed-out",action="store_true",default=None);t.add_argument("--not-timed-out",dest="timed_out",action="store_false",default=None);o=a.parse_args()
    try: claimed_exit=int(o.exit_code) if o.exit_code is not None else None
    except ValueError: claimed_exit=o.exit_code
    r=evaluate(o.receipt,o.process_status,claimed_exit,o.timed_out,o.contract,o.external_failure,o.profile,o.process_receipt,o.exit_receipt,o.command_receipt,o.process_origin,o.desktop_receipt);write(r,o.output)
    print(json.dumps({k:r[k] for k in ("process","assertionStatus","integrity","counts","binding","overallStatus","exitCode")}));return r["exitCode"]
if __name__=="__main__": raise SystemExit(main())
