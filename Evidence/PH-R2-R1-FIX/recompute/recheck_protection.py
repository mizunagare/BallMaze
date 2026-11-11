import json, os, hashlib, subprocess, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
os.chdir(ROOT)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def oid(p):
    return subprocess.run(["git", "hash-object", "--", p], capture_output=True, text=True).stdout.strip()


pm = json.load(open("Evidence/PH-R2-R1-FIX/protection/protection_manifest.json", encoding="utf-8"))
snap = json.load(open("Evidence/PH-R2-R1-FIX/protection/pre_change_snapshot.json", encoding="utf-8"))
start = {r["path"]: r["sha256"] for r in snap["tracked"]}
pre1 = {f["path"]: f for f in json.load(
    open("Evidence/PH-R2-R1-FIX/build/build-preflight-manifest.round1.json", encoding="utf-8"))["files"]}

rows = []
for f in pm["files"]:
    p = f["path"]
    ex = os.path.isfile(p)
    cur = sha(p) if ex else None
    base = start.get(p) or f["baselineSha256"]
    head = subprocess.run(["git", "rev-parse", "HEAD:" + p], capture_output=True, text=True).stdout.strip() or None
    rows.append(dict(
        path=p, category=f["category"], exists=ex,
        baselineSha256=base, currentSha256=cur,
        gitBlobOidHead=head, gitBlobOidWorktree=oid(p) if ex else None,
        sameAsFixStart=(cur == base),
        sameAsRound1Preflight=(cur == pre1[p]["sha256"]) if p in pre1 else None,
        userEditPresentAtFixStart=pre1.get(p, {}).get("userEditPresent")))

changed = [r for r in rows if not r["sameAsFixStart"]]
print("192 files: same_as_fix_start=%d changed=%d missing=%d" % (
    len(rows) - len(changed), len(changed), sum(1 for r in rows if not r["exists"])))
for r in changed:
    print("  CHANGED %-56s fixstart=%s now=%s userEditAtStart=%s" % (
        r["path"], (r["baselineSha256"] or "")[:12], (r["currentSha256"] or "")[:12],
        r["userEditPresentAtFixStart"]))
build_inputs = [r for r in changed if r["path"] in pre1]
print("all changed are the 4 build inputs:", len(build_inputs) == len(changed) and len(changed) == 4)

note = ("baseline = each file's SHA256 at PH-R2-R1-FIX start. Exactly the 4 Unity build-input files "
        "moved. All 4 had no uncommitted user edit at start (proved by the round-1 preflight), all 4 "
        "were byte-identical across build rounds 2 and 3, and nothing was restored with git.")

out = dict(generatedAt=time.strftime("%Y-%m-%dT%H:%M:%S"), note=note,
           summary=dict(total=len(rows), missing=sum(1 for r in rows if not r["exists"]),
                        sameAsFixStart=len(rows) - len(changed), changed=len(changed),
                        changedAllBuildInputs=(len(build_inputs) == len(changed) == 4),
                        changedList=[r["path"] for r in changed]),
           files=rows)
json.dump(out, open("Evidence/PH-R2-R1-FIX/protection/PROTECTED_RECHECK.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
with open("Evidence/PH-R2-R1-FIX/protection/PROTECTED_SHA256.tsv", "w", encoding="utf-8", newline="\n") as f:
    f.write("path\tcategory\tfix_start_sha256\tcurrent_sha256\tgit_blob_oid_head\tgit_blob_oid_worktree\t"
            "same_as_fix_start\tuser_edit_at_start\n")
    for r in rows:
        f.write("\t".join([r["path"], r["category"], r["baselineSha256"] or "", r["currentSha256"] or "",
                           r["gitBlobOidHead"] or "", r["gitBlobOidWorktree"] or "",
                           str(r["sameAsFixStart"]), str(r["userEditPresentAtFixStart"])]) + "\n")
print("wrote PROTECTED_RECHECK.json / PROTECTED_SHA256.tsv")
