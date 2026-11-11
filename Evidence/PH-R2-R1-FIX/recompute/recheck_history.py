import json, os, hashlib, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
os.chdir(ROOT)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


snap = json.load(open("Evidence/PH-R2-R1-FIX/protection/pre_change_snapshot.json", encoding="utf-8"))
rows = []
for it in snap["history"]:
    p = it["path"]
    ex = os.path.isfile(p)
    cur = sha(p) if ex else None
    rows.append(dict(path=p, preSha256=it["sha256"], currentSha256=cur, exists=ex,
                     verdict="MATCH" if (ex and cur == it["sha256"]) else "CHANGED"))
bad = [r for r in rows if r["verdict"] != "MATCH"]
areas = {}
for r in rows:
    k = "/".join(r["path"].split("/")[:2])
    areas.setdefault(k, [0, 0])
    areas[k][0] += 1
    if r["verdict"] != "MATCH":
        areas[k][1] += 1
print("history files=%d match=%d changed=%d missing=%d" % (
    len(rows), len(rows) - len(bad), len(bad), sum(1 for r in rows if not r["exists"])))
for r in bad[:20]:
    print("  CHANGED", r["path"])
for k, v in sorted(areas.items()):
    print("  area %-28s %4d files, %d changed" % (k, v[0], v[1]))

out = dict(generatedAt=time.strftime("%Y-%m-%dT%H:%M:%S"),
           note="PH-R1 / PH-R2 / PH-R2-R1 / PH-R2-FINAL-AUDIT evidence and the frozen INDEX/matrix "
                "must be byte-identical to the PH-R2-R1-FIX start snapshot.",
           summary=dict(files=len(rows), match=len(rows) - len(bad), changed=len(bad),
                        missing=sum(1 for r in rows if not r["exists"]),
                        areas={k: dict(files=v[0], changed=v[1]) for k, v in areas.items()}),
           files=rows)
json.dump(out, open("Evidence/PH-R2-R1-FIX/protection/HISTORY_RECHECK.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote HISTORY_RECHECK.json")
